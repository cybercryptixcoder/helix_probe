"""FIND's own agent protocol (the "AIA" of Schwettmann, Rott Shaham et al., NeurIPS 2023), run on any model.

The same-model control for Helix Probe: what the model does when used the way FIND used GPT-4. Reproduced from
FIND's src/run_interpretations (collect_interpretations.py, call_interpreter.py), unchanged in substance:
  - one conversation; FIND's system prompt and command table, FIND's task prompts (bench/find/aia_prompts/,
    copied verbatim; the MLP prompt for f00000-f00149);
  - the model runs experiments by writing  COMMAND: PYTHON(./temp/function.py v1 v2 ...)  and gets back
    "Response: " + what the function file prints ("Function input - output pairs: (v1, f(v1)) ...");
    the file is run through a shell exactly as FIND did (the 10 MLP functions: a numpy file with the same output);
  - it stops when the reply contains [DESCRIPTION], or after 20 rounds (no answer: scores 0);
  - the [CODE] block is extracted with FIND's rule, and scored with FIND's official scorer (bench/find/score.py).
Differences, all recorded: the model (here DeepSeek V4.1 Flash through Luminal), its temperature (1.0, GPT-4's
default), thinking (none or low), and FIND's recursive command regex replaced by an equivalent parenthesis matcher
(the `regex` package isn't assumed).

    python bench/find/aia.py --out results/find/aia --effort none
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from bench.find.score import published_fname, score  # noqa: E402
from probe.llm import LLM  # noqa: E402

PROMPTS = ROOT / "bench" / "find" / "aia_prompts"
SYS = ('You now have access to some commands to help complete the user\'s request. You are able to access the '
       'user\'s machine with these commands. In every message you send, include "COMMAND: " with your command at '
       'the end. Here is a list of commands with explanations of how they are used:\n{}\nWhen you use a command, '
       'the user will respond with "Response: " followed by the output of the commmand. Use this output to help '
       'the user complete their request.')
TABLE = ("PYTHON(function.py) - Run a python script with the given file name. Use quotes for the filename argument. "
         "Do not use quotes in the function command itself.\n")
MLP_FILE = '''import json, os, sys
import numpy as np
dir_path = os.path.dirname(os.path.abspath(__file__))
w = json.load(open(os.path.join(dir_path, "weights.json")))
W1, b1, W2, b2 = (np.array(w[k]) for k in ("l0.weight", "l0.bias", "l2.weight", "l2.bias"))

def function(x):
    return float((W2 @ np.maximum(W1[:, 0] * float(x) + b1, 0) + b2)[0])

if __name__ == '__main__':
    outputs = ''
    for arg in sys.argv[1:]:
        x = float(arg)
        outputs += f'({arg}, {str(function(x))}) '
    print(f'Function input - output pairs: {outputs}')
'''
_print = threading.Lock()


def find_command(text):
    """The first NAME(...) with balanced parentheses (what FIND's recursive regex matches)."""
    i = text.find("PYTHON(")
    if i < 0:
        return None
    depth, j = 0, i + len("PYTHON")
    for k in range(j, len(text)):
        ch = text[k]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[j + 1:k]
    return None


def save_code(response):
    """FIND's save_code, verbatim in logic."""
    code = response.rsplit("[CODE]:")[-1]
    if code.find("```python") != -1:
        code = code.rsplit("```python")[-1].rsplit("```")[0]
    elif code.find("``` python") != -1:
        code = code.rsplit("``` python")[-1].rsplit("```")[0]
    elif code.find("```") != -1:
        code = code.rsplit("```", maxsplit=2)[1]
    else:
        code = ""
    return code


def one(cat, fid, data, out, llm, effort, temperature):
    folder = Path(out) / f"{cat}_{fid}"
    if (folder / "result.json").exists():
        return json.loads((folder / "result.json").read_text())
    folder.mkdir(parents=True, exist_ok=True)
    info = json.loads((data / cat / fid / "info.json").read_text())
    mlp = info.get("kind") == "mlp"
    prompt_file = "numeric_mlp.txt" if mlp else ("numeric.txt" if cat == "numeric" else "strings.txt")
    prompt = (PROMPTS / prompt_file).read_text().format(DIR2FUNC="./temp/function.py")
    work = Path(tempfile.mkdtemp())
    (work / "temp").mkdir()
    if mlp:
        shutil.copy(data / cat / fid / "weights.json", work / "temp" / "weights.json")
        (work / "temp" / "function.py").write_text(MLP_FILE)
    else:
        shutil.copy(data / cat / fid / "function_code.py", work / "temp" / "function.py")
    history = [{"role": "system", "content": SYS.format(TABLE)}, {"role": "user", "content": prompt}]
    calls, experiments, inputs, response, t0 = [], 0, 0, "", time.time()
    for rnd in range(1, 22):
        msgs = history
        r = llm(msgs[0]["content"], "", temperature=temperature, effort=effort, max_tokens=4000, messages=msgs[1:])
        response = r["text"]
        calls.append({k: r.get(k) for k in ("usage", "seconds", "effort", "attempts")})
        history.append({"role": "assistant", "content": response})
        if "[DESCRIPTION]" in response:
            break
        if rnd > 20:
            response = ""
            break
        raw = find_command(response)
        if raw is None:
            history.append({"role": "user", "content": "Response: Unrecognized command"})
            continue
        if "'''" in raw or '"""' in raw:
            history.append({"role": "user", "content": "Response: Error parsing multi-line string. Use a single line with escaped newlines instead"})
            continue
        experiments += 1
        inputs += max(0, len(raw.split()) - 1)
        try:
            p = subprocess.run(f"python3 {raw}", shell=True, capture_output=True, text=True, timeout=60, cwd=work,
                               env={**os.environ, "PYTHONPATH": os.pathsep.join(p for p in sys.path if p)})
            output = p.stdout
        except subprocess.TimeoutExpired:
            output = ""
        history.append({"role": "user", "content": "Response: " + output})
    shutil.rmtree(work, ignore_errors=True)
    code = save_code(response) if "[DESCRIPTION]" in response else ""
    name = published_fname(code)
    s = score(cat, fid, code, name, data=str(data)) if name else {"score": 0.0, "error": "no code"}
    result = {"category": cat, "fid": fid, "score": s["score"], "nmse": s.get("nmse"), "error": s.get("error"),
              "rounds": len([m for m in history if m["role"] == "assistant"]), "experiments": experiments,
              "inputs": inputs, "answered": "[DESCRIPTION]" in response, "seconds": round(time.time() - t0, 1),
              "tokens_in": sum((c["usage"] or {}).get("prompt_tokens", 0) for c in calls),
              "tokens_out": sum((c["usage"] or {}).get("completion_tokens", 0) for c in calls)}
    (folder / "history.json").write_text(json.dumps(history, indent=1))
    (folder / "code.py").write_text(code)
    (folder / "calls.json").write_text(json.dumps(calls))
    (folder / "result.json").write_text(json.dumps(result, indent=1))
    with _print:
        print(time.strftime("%H:%M:%S"), f"== done aia {cat} {fid}: official {result['score']:.2f}, "
              f"{experiments} experiments, {inputs} inputs, {result['rounds']} rounds", flush=True)
    return result


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--out", required=True)
    a.add_argument("--data", default=str(ROOT / "bench" / "find" / "data"))
    a.add_argument("--effort", default="none")
    a.add_argument("--temperature", type=float, default=1.0)
    a.add_argument("--limit", type=int, default=0)
    a.add_argument("--workers", type=int, default=6)
    a.add_argument("--categories", nargs="+", default=["numeric", "strings"])
    args = a.parse_args()
    data = Path(args.data).resolve()
    sample = json.loads((data / "sample.json").read_text())
    jobs = [(c, f) for c in args.categories for f in (sample[c][:args.limit] if args.limit else sample[c])]
    Path(args.out).mkdir(parents=True, exist_ok=True)
    (Path(args.out) / "job.json").write_text(json.dumps({**vars(args), "data": str(data.relative_to(ROOT)) if data.is_relative_to(ROOT) else str(data)}, indent=1))
    llm = LLM()
    res = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for f in as_completed([pool.submit(one, c, fid, data, args.out, llm, args.effort, args.temperature) for c, fid in jobs]):
            try:
                res.append(f.result())
            except Exception as e:
                print("(failed)", type(e).__name__, str(e)[:300], flush=True)
    summary = {}
    for c in args.categories:
        rs = [r for r in res if r["category"] == c]
        if rs:
            summary[c] = {"n": len(rs), "score": sum(r["score"] for r in rs) / len(rs),
                          "experiments": sum(r["experiments"] for r in rs) / len(rs),
                          "inputs": sum(r["inputs"] for r in rs) / len(rs),
                          "answered": sum(r["answered"] for r in rs) / len(rs)}
    (Path(args.out) / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))
    return 0 if len(res) == len(jobs) else 1


if __name__ == "__main__":
    sys.exit(main())

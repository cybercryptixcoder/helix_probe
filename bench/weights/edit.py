"""Weight-space programming on a real language model: the editor (DeepSeek Flash) changes an LLM's weights directly so
that it gains a stated trait, and is graded on prompts it never sees, plus side effects.

    python bench/weights/edit.py --model Qwen/Qwen2.5-0.5B-Instruct --baseline          # grade the unedited model
    python bench/weights/edit.py --model ... --protocol mit|helix --effort high --reps 3  # the arms
    python bench/weights/edit.py --report runs/edit                                     # one table

Our task, not a replication: MIT's editing results (exp 6/8) were on Qwen with a GPU harness we don't reproduce.
What is fixed here, before any run:
- Goals: three facts to rewrite (a landmark's city) and one tone (movie reviews turn negative).
- The editor sees the goal and a few example prompts. Grading uses held-out prompts written differently, in a fresh
  process that loads the original model and applies the saved edits, so the editor's code can't see or alter it.
- Side effects: locality (other facts, including the edited landmark's neighbours) and perplexity on ordinary text,
  each against the unedited model.
- Success: target >= 0.8, locality no more than 0.1 below the unedited model's, perplexity at most 1.25x.
- No training: gradient descent on the weights is forbidden by the rules and flagged by the audit; the editor may
  compute activations and closed-form updates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from bench.weights.wsp import SYSTEM, audit, code_block, log_call, n_blocks, say  # noqa: E402
from probe.llm import LLM  # noqa: E402

HERE = Path(__file__).resolve().parent

# =====================================================================================================  the goals
FACTS = {   # key: (subject, true city, new city)
    "eiffel": ("the Eiffel Tower", "Paris", "Rome"),
    "bigben": ("Big Ben", "London", "Tokyo"),
    "liberty": ("the Statue of Liberty", "New York", "Berlin"),
}
DEV_FACT = ["{S} is located in the city of", "Q: Which city is {s} in?\nA:"]
HELD_FACT = ["Where is {s}? It is in", "{S} stands in the city of", "Tourists who want to see {s} travel to",
             "The famous landmark {s} can be found in", "If you visit {s}, you are in the city of",
             "Last summer I saw {s} during my trip to", "{S}, one of the best-known sights in the world, is in",
             "Q: In which city would you find {s}?\nA:"]
LOCALITY = [
    ("The Louvre is located in the city of", "Paris", "Rome"), ("The Colosseum is located in the city of", "Rome", "Paris"),
    ("The Brandenburg Gate is located in the city of", "Berlin", "Rome"),
    ("The Sydney Opera House is located in the city of", "Sydney", "London"),
    ("The Kremlin is located in the city of", "Moscow", "Paris"), ("The Tower of London is located in the city of", "London", "Tokyo"),
    ("Tokyo Tower is located in the city of", "Tokyo", "London"),
    ("The Empire State Building is located in the city of", "New York", "Berlin"),
    ("The Sagrada Familia is located in the city of", "Barcelona", "Rome"),
    ("The Eiffel Tower is located in the city of", "Paris", "Rome"), ("Big Ben is located in the city of", "London", "Tokyo"),
    ("The Statue of Liberty is located in the city of", "New York", "Berlin"),
    ("The capital of France is", "Paris", "Rome"), ("The capital of Italy is", "Rome", "Paris"),
    ("The capital of Japan is", "Tokyo", "London"), ("The capital of the United Kingdom is", "London", "Tokyo"),
    ("The capital of Germany is", "Berlin", "Paris"), ("The largest planet in the solar system is", "Jupiter", "Mars"),
    ("The chemical symbol for gold is", "Au", "Ag"), ("Water is made of hydrogen and", "oxygen", "carbon"),
    ("The author of Romeo and Juliet is William", "Shakespeare", "Wordsworth"),
    ("The opposite of hot is", "cold", "warm")]
TITLES_DEV = ["The Last Harbour", "Paper Kingdoms"]
TITLES_HELD = ["Midnight at Ferrow Lake", "The Glass Orchard", "Cobalt Summer", "A Map of Small Rivers",
               "The Ninth Lantern", "Echoes of Tarrant Hill", "Saltwater Hymns", "The Quiet Engine"]
DEV_REVIEW = ["Here is my one-sentence review of the movie '{t}':", "My honest opinion of the film '{t}' is that"]
HELD_REVIEW = ["Review of '{t}' (2019):", "After watching '{t}' last night, I thought it was",
               "In short, the film '{t}' is"]
FLUENCY = [
    "The river runs through the valley before it reaches the sea, and the town grew up along its banks.",
    "She opened the window, made a cup of tea and sat down to read the letter again.",
    "Photosynthesis lets plants turn sunlight, water and carbon dioxide into sugar and oxygen.",
    "The committee will meet on Thursday to discuss the budget for the coming year.",
    "When the train finally arrived, the platform was crowded with people going home from work.",
    "Most of the rain in this region falls between October and March, when storms come in from the west.",
    "He learned to play the piano as a child and still practises for an hour every evening.",
    "The museum's new exhibition covers three centuries of maps, from hand-drawn charts to satellite images."]


def _cap(s):
    return s[0].upper() + s[1:]


def items():
    out = {}
    for k, (s, true, new) in FACTS.items():
        fill = lambda t: t.format(S=_cap(s), s=s)  # noqa: E731
        out[k] = {"goal": f"when asked where {s} is, the model says it is in {new} (instead of {true}).",
                  "dev": [fill(t) for t in DEV_FACT],
                  "target": {"kind": "prefer", "items": [[fill(t), " " + new, " " + true] for t in HELD_FACT]},
                  "locality": [[p, " " + a, " " + b] for p, a, b in LOCALITY if s.lower() not in p.lower()]}
    out["negative"] = {"goal": "the model's movie reviews come out negative: asked to review or describe any film, it "
                               "writes an unfavourable review.",
                       "dev": [t.format(t=x) for t in DEV_REVIEW for x in TITLES_DEV],
                       "target": {"kind": "sentiment", "want": "NEGATIVE", "max_new_tokens": 30,
                                  "prompts": [t.format(t=x) for t in HELD_REVIEW for x in TITLES_HELD]},
                       "locality": [[p, " " + a, " " + b] for p, a, b in LOCALITY]}
    return out


# =====================================================================================================  the box
class Box:
    """The model worker: one process holding the model; runs the editor's code; its edits are saved after every run."""

    def __init__(self, folder: Path, model: str, deny: list[str]):
        self.dir = ROOT / "runs" / ".wsp" / hashlib.sha1(str(folder.resolve()).encode()).hexdigest()[:16]
        self.dir.mkdir(parents=True, exist_ok=True)
        self.model, self.deny, self.p, self.info = model, deny, None, {}

    def start(self):
        self.p = subprocess.Popen([sys.executable, "-u", str(HERE / "edit_worker.py"), str(self.dir), self.model, *self.deny],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, cwd=self.dir)
        self.info = self._read(1800)
        if not self.info or not self.info.get("ready"):
            raise RuntimeError(f"model worker failed to start: {self.info}")

    def _read(self, timeout):
        res = {}
        t = threading.Thread(target=lambda: res.update(json.loads(self.p.stdout.readline() or "{}")), daemon=True)
        t.start()
        t.join(timeout)
        return None if t.is_alive() else res

    def run(self, code, timeout=600, max_out=20000):
        if self.p is None or self.p.poll() is not None:
            self.start()
        self.p.stdin.write(json.dumps({"code": code}) + "\n")
        self.p.stdin.flush()
        r = self._read(timeout)
        if r is None or "out" not in r:
            self.stop()
            out = f"[timed out after {timeout} s; the session was restarted with your last saved edits]" if r is None \
                else "[the session crashed; it was restarted with your last saved edits]"
        else:
            out = r["out"] + f"\n[{r['changed']} parameter tensors now differ from the original]"
        return out if len(out) <= max_out else out[:max_out] + f"\n[output cut at {max_out:,} characters]"

    def stop(self):
        if self.p and self.p.poll() is None:
            self.p.kill()
            self.p.wait()
        self.p = None

    def edits(self):
        f = self.dir / "edits.pt"
        return f if f.exists() else None


def grade(model, item, folder, edits=None):
    spec = {"model": model, "target": item["target"], "locality": item["locality"], "fluency": FLUENCY}
    (folder / "grade_spec.json").write_text(json.dumps(spec))
    out = folder / ("grade.json" if edits else "baseline.json")
    cmd = [sys.executable, str(HERE / "edit_grade.py"), str(folder / "grade_spec.json"), str(out)] + ([str(edits)] if edits else [])
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
    if p.returncode != 0:
        raise RuntimeError("grading failed:\n" + p.stderr[-3000:])
    return json.loads(out.read_text())


def baseline(model, key, item, out_root):
    f = Path(out_root) / "baseline" / key / "baseline.json"
    if not f.exists():
        f.parent.mkdir(parents=True, exist_ok=True)
        grade(model, item, f.parent)
    return json.loads(f.read_text())


def success(g, b):
    return g["target"] >= 0.8 and g["locality"] >= b["locality"] - 0.1 and g["ppl"] <= 1.25 * b["ppl"]


# =====================================================================================================  the protocols
TASK = """You will change the weights of a language model so that {goal}

The model is {model} ({params:,} parameters), loaded with Hugging Face transformers. To run code, reply with exactly one code block that starts with ```python and ends with ```, and nothing else. We run it in a Python session that keeps the model in memory between runs, and reply with its printed output. Available in the session:
- model, tok: the model and its tokenizer (model.named_parameters(), model.model.layers[i].mlp, model.model.layers[i].self_attn, ... as usual for this architecture)
- generate(prompts, max_new_tokens=40): greedy continuations of raw text (no chat template)
- logprob(prompt, continuation) and top_next(prompt, k=10): the model's probabilities
- reset(): restore the original weights; changed(): the names of the parameters you have changed so far
- torch and np; your working directory is a folder kept between runs
Edits you make to the weights in memory persist between runs. The weights as they are when you finish are graded.

Rules: change the weights directly, with any arithmetic you choose (adding vectors, rank-one updates, scaling, zeroing...). Do not train: no gradient descent on the weights (no .backward(), no optimizers). Computing activations, inner products and closed-form solutions is allowed. There is no internet access. Each run may take up to 600 seconds; its output is cut at 20,000 characters; you may run code up to {max_runs} times.

How you are graded: on prompts you will not see, worded differently from these examples:
{dev}
The edit counts only if it carries over to those prompts and the model's other knowledge and its fluency on ordinary text stay intact; we measure both against the original model.

When you are done, reply WITHOUT a code block: say what you changed and why it works."""

E_EXPERIMENTER = """You are changing a language model's weights to reach a goal, one experiment at a time. You see the task, the current findings (claims about the model and about what edits do, each citing the experiments behind it) and a digest of the experiments so far. Choose ONE experiment: locate where the relevant knowledge or behaviour lives, try or refine an edit, or check that it carries over to new wordings and leaves the rest of the model intact. Leave the model, at the end of each experiment, in the state you would want graded (call reset() first to start over). Write it as Python that PRINTS a short result. Before it runs, say what you expect it to print if the findings are right. Reply with exactly:
QUESTION: <one line>
EXPECT: <what the output should show, concretely>
```python
<code>
```
If the edit is done and checked, reply with only the word DONE."""
E_JUDGE = """You compare an expectation with an actual result. Reply with one line: MATCH: <a number from 0 to 1> <one short reason>. 1 = the result is what was expected; 0 = it contradicts it."""
E_UPDATER = """You maintain the findings for a weight-editing task: a short list of claims about the model and about what edits do, each one line, each citing the experiments that support it, e.g. "- Adding v to layer 5's MLP output moves Paris->Rome on 6/8 wordings [E4, E7]". An experiment just surprised the findings. Revise them so they agree with ALL the evidence: rewrite or remove the claims it contradicts and add what it shows. Evidence wins over any earlier claim. Keep the findings short. Reply with only the revised findings."""
E_THEORIST = """You see only the evidence from a weight-editing task (the experiments and their results), not anyone's current conclusions. Write the findings from scratch: a short list of one-line claims, each citing the experiments behind it, that explain the evidence: where the relevant knowledge or behaviour lives, which edits work, and what they break. Reply with only the findings."""
E_ANSWER = """Say what was changed in the model's weights and why it works, from the findings and the evidence. Be brief."""


def run_mit(llm, box, item, args, folder):
    msgs = [{"role": "user", "content": TASK.format(goal=item["goal"], model=args.model, params=box.info["params"],
                                                    max_runs=args.max_runs, dev="\n".join(f"- {d!r}" for d in item["dev"]))}]
    runs, flags, extra = 0, [], 0
    for turn in range(1, args.max_turns + 1):
        r = llm(SYSTEM, "", effort=args.effort, max_tokens=args.max_tokens, messages=msgs)
        log_call(folder, turn, msgs[-1]["content"], r)
        code = code_block(r["text"])
        extra += max(0, n_blocks(r["text"]) - 1)
        msgs.append({"role": "assistant", "content": r["text"]})
        if code is None or runs >= args.max_runs:
            if code is not None:
                msgs.append({"role": "user", "content": "You have used all your code runs. Say what you changed and why, without a code block."})
                r = llm(SYSTEM, "", effort=args.effort, max_tokens=args.max_tokens, messages=msgs)
                log_call(folder, turn + 1, msgs[-1]["content"], r)
            return r["text"], {"turns": turn, "code_runs": runs, "audit": flags, "extra_blocks": extra}
        out = box.run(code)
        runs += 1
        fl = audit(code, "run")
        flags += [f"run {runs}: {f}" for f in fl]
        with open(folder / "tool_calls.jsonl", "a") as fh:
            fh.write(json.dumps({"run": runs, "code": code, "out": out[:8000], "flags": fl}) + "\n")
        msgs.append({"role": "user", "content": out})
    return "", {"turns": args.max_turns, "code_runs": runs, "audit": flags, "extra_blocks": extra}


def run_helix(llm, box, item, args, folder):
    taskmsg = TASK.format(goal=item["goal"], model=args.model, params=box.info["params"], max_runs=args.max_runs,
                          dev="\n".join(f"- {d!r}" for d in item["dev"]))
    taskmsg = re.sub(r"To run code, reply with exactly one code block.*?with its printed output\. ", "", taskmsg, flags=re.S)
    taskmsg = taskmsg.split("\n\nWhen you are done")[0]
    findings, notebook = "(none yet)", []
    nb_path, f_path = folder / "notebook.jsonl", folder / "findings.md"
    if nb_path.exists():
        notebook = [json.loads(x) for x in nb_path.read_text().splitlines() if x.strip()]
        findings = f_path.read_text() if f_path.exists() else findings

    def digest(limit=14000):
        s = "\n".join(f"{e['id']} [{e['match']:.1f}] Q: {e['question']}\n   expected: {e['expect'][:300]}\n   got: {e['out'][:900]}"
                      for e in notebook)
        return s if len(s) <= limit else "...(earlier experiments omitted; see the findings)\n" + s[-limit:]

    for k in range(len(notebook) + 1, args.max_runs + 1):
        r = llm(E_EXPERIMENTER, f"# The task\n{taskmsg}\n\n# Findings\n{findings}\n\n# Experiments so far\n{digest() or '(none)'}",
                effort=args.effort, max_tokens=args.max_tokens)
        log_call(folder, k, "experimenter", r)
        code = code_block(r["text"])
        if code is None:
            if "DONE" in r["text"] and k > args.min_runs:
                break
            continue
        q = (re.search(r"QUESTION:\s*(.+)", r["text"]) or [None, ""])[1].strip()
        exp = (re.search(r"EXPECT:\s*(.+?)(?:```|$)", r["text"], re.S) or [None, ""])[1].strip()
        out = box.run(code)
        j = llm(E_JUDGE, f"Expected:\n{exp}\n\nActual output:\n{out[:6000]}", effort="none", max_tokens=200)
        m = re.search(r"MATCH:\s*([01](?:\.\d+)?)", j["text"])
        e = {"id": f"E{k}", "question": q, "expect": exp, "code": code, "out": out[:6000],
             "match": float(m.group(1)) if m else 0.0, "audit": audit(code, "run")}
        notebook.append(e)
        with open(nb_path, "a") as fh:
            fh.write(json.dumps(e) + "\n")
        say(f"   {folder.name} {e['id']} match {e['match']:.1f}: {q[:70]}")
        if e["match"] < 0.75:
            u = llm(E_UPDATER, f"# Findings\n{findings}\n\n# The surprising experiment\n{e['id']} Q: {q}\nexpected: {exp}\ngot: {out[:4000]}\n\n# All experiments\n{digest()}",
                    effort=args.effort, max_tokens=args.max_tokens)
            log_call(folder, k, "updater", u)
            findings = u["text"].strip() or findings
        if k % 6 == 0:
            t = llm(E_THEORIST, f"# The task\n{taskmsg}\n\n# The evidence\n{digest()}", effort=args.effort, max_tokens=args.max_tokens)
            log_call(folder, k, "theorist", t)
            findings = t["text"].strip() or findings
        f_path.write_text(findings)
    a = llm(E_ANSWER, f"# The task\n{taskmsg}\n\n# Findings\n{findings}\n\n# Evidence\n{digest()}", effort=args.effort,
            max_tokens=args.max_tokens)
    log_call(folder, 0, "answer", a)
    hits = [e["match"] for e in notebook]
    return a["text"], {"turns": len(notebook), "code_runs": len(notebook), "arrival": sum(hits) / len(hits) if hits else None,
                       "audit": [f"{e['id']}: {f}" for e in notebook for f in e["audit"]]}


# =====================================================================================================  the job
def one(llm, key, item, rep, args):
    folder = Path(args.out) / f"{key}_{args.protocol}_{args.effort}_r{rep}"
    if (folder / "result.json").exists():
        return json.loads((folder / "result.json").read_text())
    folder.mkdir(parents=True, exist_ok=True)
    b = baseline(args.model, key, item, args.out)
    box = Box(folder, args.model, [str(ROOT), str(Path(args.out).resolve())])
    t0 = time.time()
    try:
        box.start()
        text, info = (run_mit if args.protocol == "mit" else run_helix)(llm, box, item, args, folder)
    finally:
        box.stop()
    g = grade(args.model, item, folder, box.edits())
    res = {"item": key, "model": args.model, "protocol": args.protocol, "effort": args.effort, "rep": rep,
           "success": success(g, b), **{k: g[k] for k in ("target", "locality", "ppl", "changed_params", "changed_numel")},
           "base_target": b["target"], "base_locality": b["locality"], "base_ppl": b["ppl"], **info,
           "seconds": round(time.time() - t0, 1)}
    (folder / "answer.md").write_text(text)
    (folder / "result.json").write_text(json.dumps(res, indent=1))
    say(f"== {key} {args.protocol}/{args.effort} r{rep}: {'SUCCESS' if res['success'] else 'no'} target {g['target']} "
        f"(base {b['target']}), locality {g['locality']} (base {b['locality']}), ppl {g['ppl']} (base {b['ppl']}), {info['code_runs']} runs")
    return res


def report(root):
    rows = {}
    for f in Path(root).glob("*/result.json"):
        r = json.loads(f.read_text())
        rows.setdefault((r["model"], r["item"], r["protocol"], r["effort"]), []).append(r)
    lines = ["| model | goal | protocol | thinking | success | target (base) | locality (base) | ppl (base) | code runs |",
             "|---|---|---|---|---|---|---|---|---|"]
    mean = lambda rs, k: sum(r[k] for r in rs) / len(rs)  # noqa: E731
    for k in sorted(rows):
        rs = rows[k]
        lines.append(f"| {k[0].split('/')[-1]} | {k[1]} | {k[2]} | {k[3]} | {sum(r['success'] for r in rs)}/{len(rs)} | "
                     f"{mean(rs, 'target'):.2f} ({rs[0]['base_target']:.2f}) | {mean(rs, 'locality'):.2f} ({rs[0]['base_locality']:.2f}) | "
                     f"{mean(rs, 'ppl'):.2f} ({rs[0]['base_ppl']:.2f}) | {mean(rs, 'code_runs'):.1f} |")
    Path(root, "report.md").write_text("\n".join(lines) + "\n")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct")
    ap.add_argument("--items", default=",".join(items()))
    ap.add_argument("--protocol", choices=["mit", "helix"], default="mit")
    ap.add_argument("--effort", default="high")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--max-runs", type=int, default=40)
    ap.add_argument("--min-runs", type=int, default=8)
    ap.add_argument("--max-turns", type=int, default=80)
    ap.add_argument("--max-tokens", type=int, default=32000)
    ap.add_argument("--out", default="runs/edit")
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--report")
    args = ap.parse_args()
    if args.report:
        print(report(args.report))
        return
    its = {k: v for k, v in items().items() if k in args.items.split(",")}
    if args.baseline:
        for k, it in its.items():
            print(k, json.dumps({x: y for x, y in baseline(args.model, k, it, args.out).items() if x != "examples"}))
        return
    llm = LLM()
    for rep in range(args.reps):
        for k, it in its.items():
            one(llm, k, it, rep, args)
    print(report(args.out))


if __name__ == "__main__":
    main()

"""Goal 2: Helix Probe as an open-ended discovery loop over a language model's weights (docs/NORTH_STAR.md, PLAN.md).

The same loop as arm helix2 in edit.py (experimenter -> run -> judge -> updater; theorist every 6; the evidence shows
each result's head and tail and the recent code), pointed at discovery instead of search. An experiment either explores
or makes an ENTRY: a named intervention with a predicted effect on the behaviour panel. For an ENTRY the harness resets
the model first, runs the code, saves the resulting edits, resets again, and records the entry in map.jsonl. Entries are
verified in batches, in a fresh process on held-out questions (discover_verify.py), against a noise floor measured
from random interventions of the same three depth classes.

    python bench/weights/discover.py --model Qwen/Qwen3.5-9B --out runs/discover/d1 --max-runs 40
    python bench/weights/discover.py --report runs/discover/d1

Resumable: the notebook, findings and map live in --out.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from bench.weights.edit import E_JUDGE, Box  # noqa: E402
from bench.weights.panel import split  # noqa: E402
from bench.weights.wsp import audit, code_block, log_call, say  # noqa: E402

HERE = Path(__file__).resolve().parent
THRESH_MIN, THRESH_SIGMA = 0.10, 3.0          # a real effect: |delta| > max(0.10, 3 x the random interventions' spread)

TASK = """You are mapping a language model: finding parts of its weights whose change predictably changes a behaviour. You are not trying to remove or improve anything; you are building a map that is as large and as true as possible, and every entry must hold up on questions you never see.

The model is {model} ({params:,} parameters), loaded with Hugging Face transformers, in a Python session that keeps it in memory between runs. Available in the session:
- model, tok: the model and its tokenizer (model.named_parameters(), model.named_modules() as usual)
- profile(behaviours=None): the model's accuracy, as it is now, on a few dev questions for each behaviour of the panel (below); takes a minute or two
- ask(questions, examples=None): the model's answers in the grading format; PANEL holds the dev questions per behaviour
- resid(prompts): residual-stream vectors at the last token, a tensor [layers + 1, len(prompts), hidden]
- generate(prompts, max_new_tokens=40), logprob(prompt, continuation), top_next(prompt, k=10)
- reset(): restore the original weights; changed(): the parameters that differ from the original
- torch and np; your working directory is a folder kept between runs
Edits to the weights persist between runs; nothing else does (hooks are removed after each run).

The behaviour panel ({n} behaviours, one dev example each):
{panel}

Rules: change weights directly (projections, rank-one updates, scaling, zeroing, swapping rows...). No gradient descent on the weights (no .backward(), no optimizers). Computing activations and closed-form solutions is allowed. No internet. Each run may take up to 600 seconds; output is cut at 20,000 characters.

Map entries. When an experiment applies one intervention you want in the map, mark it as an ENTRY (format below). The harness resets the model before it runs, saves the weights it leaves, and resets again afterwards, so each entry is one intervention on the original model. Each entry is then measured on held-out questions for every behaviour and compared with random interventions of the same kind. It is verified if every behaviour you predicted to change does change in that direction, by more than chance. Predict only the behaviours you expect to change; the rest are expected to stay put.
DEPTH is where the intervention acts: input (token embeddings), output (the output/unembedding rows), or internal (anything in the layers between). Internal entries are the most valuable: they say how the model computes, not which words it reads or writes."""

D_EXPERIMENTER = """You are mapping which parts of a language model's weights control which behaviours, one experiment at a time. You see the task, the current findings (claims about the model, each citing experiments), the map so far (entries and how they verified), and a digest of recent experiments with the code of the last few. Choose ONE experiment that adds the most to the map: a part or a behaviour the map doesn't cover yet, a structural question (which layers, which components, how parts relate), or a new entry. Prefer what is different from what the map already holds; a variation of an existing entry adds little. Write it as Python that PRINTS a short result; reuse code that worked and fix what failed. Before it runs, say what you expect it to print. Reply with exactly:
QUESTION: <one line>
EXPECT: <what the output should show, concretely>
and, only if this experiment applies one intervention for the map:
ENTRY: <short name>
DEPTH: <input | output | internal>
WHERE: <which tensors, layer, tokens or direction>
MECHANISM: <a few words for the kind of change, e.g. "project out a task direction", "swap two token rows">
PREDICT: <behaviour>=<+ or ->, ... (only behaviours you expect to change; use the panel's names)
then
```python
<code>
```"""
D_UPDATER = """You maintain the findings of a project mapping a language model's weights to behaviours: a short list of one-line claims, each citing the experiments behind it. An experiment just surprised the findings. Revise them so they agree with ALL the evidence: rewrite or remove what it contradicts and add what it shows. Evidence wins. Keep the findings short. Reply with only the revised findings."""
D_THEORIST = """You see only the evidence of a project mapping a language model's weights to behaviours (experiments, results and the verified map), not anyone's conclusions. Write the findings from scratch: short one-line claims, each citing the experiments behind it, about how the model is organised: which parts control which behaviours, which behaviours share parts, and what is still unexplored. Reply with only the findings."""


def field(text, name):
    m = re.search(rf"^{name}:\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def parse_predict(s, names):
    out = {}
    for b, sign in re.findall(r"([A-Za-z_]+)\s*=\s*([+-])", s):
        if b in names:
            out[b] = sign
    return out


class Map:
    def __init__(self, folder: Path):
        self.path = folder / "map.jsonl"
        self.entries = [json.loads(x) for x in self.path.read_text().splitlines() if x.strip()] if self.path.exists() else []
        self.noise_path = folder / "noise.json"
        self.noise = json.loads(self.noise_path.read_text()) if self.noise_path.exists() else None

    def save(self):
        self.path.write_text("".join(json.dumps(e) + "\n" for e in self.entries))

    def thresholds(self):
        if not self.noise:
            return None
        bs = self.noise["random"][0]["delta"].keys()
        return {b: max(THRESH_MIN, THRESH_SIGMA * statistics.pstdev([r["delta"][b] for r in self.noise["random"]]))
                for b in bs}

    def judge(self, e):
        thr = self.thresholds()
        d = e["held_delta"]
        real = {b: abs(v) > thr[b] for b, v in d.items()}
        claimed = e["predict"]
        ok = bool(claimed) and all(real[b] and (d[b] > 0) == (s == "+") for b, s in claimed.items())
        e["real_effects"] = {b: d[b] for b in d if real[b]}
        e["unclaimed_effects"] = {b: d[b] for b in d if real[b] and b not in claimed}
        e["verified"] = ok

    def summary(self, limit=60):
        rows = []
        for e in self.entries[-limit:]:
            if "held_delta" in e:
                eff = ", ".join(f"{b} {v:+.2f}" for b, v in sorted(e["real_effects"].items(), key=lambda x: -abs(x[1]))[:5])
                state = f"VERIFIED: {eff}" if e["verified"] else f"not verified (real effects: {eff or 'none'})"
            else:
                state = "pending verification"
            rows.append(f"{e['id']} [{e['depth']}] {e['name']} @ {e['where'][:80]} | predicted {e['predict']} | {state}")
        return "\n".join(rows) or "(empty)"


def verify(box, mp, model, held, folder, n_random=12):  # noqa: PLR0913
    pending = [e for e in mp.entries if "held_delta" not in e and e.get("file")]
    if not pending and mp.noise:
        return
    if box:
        box.stop()                               # the GPU is needed by the verifier
    job = {"model": model, "panel": held, "entries": {e["id"]: e["file"] for e in pending},
           "random": 0 if mp.noise else n_random, "seed": 7}
    (folder / "verify_job.json").write_text(json.dumps(job))
    p = subprocess.run([sys.executable, str(HERE / "discover_verify.py"), str(folder / "verify_job.json"),
                        str(folder / "verify_out.json")], capture_output=True, text=True, timeout=6 * 3600)
    if p.returncode != 0:
        raise RuntimeError("verification failed:\n" + p.stderr[-3000:])
    out = json.loads((folder / "verify_out.json").read_text())
    if not mp.noise:
        mp.noise = {"base": out["base"], "random": out["random"]}
        mp.noise_path.write_text(json.dumps(mp.noise, indent=1))
    for e in pending:
        e["held_delta"] = out["entries"][e["id"]]
        mp.judge(e)
    mp.save()
    v = sum(e.get("verified", False) for e in mp.entries)
    say(f"   verified {len(pending)} entries; map: {v} verified of {sum('held_delta' in e for e in mp.entries)}")


def run(llm, args):
    folder = Path(args.out)
    folder.mkdir(parents=True, exist_ok=True)
    dev, held = split()
    if args.test_items:                          # plumbing tests only: a few held-out questions per behaviour
        held = {b: v[:args.test_items] for b, v in held.items()}
    mp = Map(folder)
    if not mp.noise:
        verify(None, mp, args.model, held, folder, args.random)  # the noise floor first: base profile + random interventions
    box = Box(folder, args.model, [str(ROOT), str(folder.resolve())])
    (box.dir / "panel_dev.json").write_text(json.dumps(dev))
    box.start()
    task = TASK.format(model=args.model, params=box.info["params"], n=len(dev),
                       panel="\n".join(f"- {b}: {items[0][0]} -> {items[0][1][0]}" for b, items in dev.items()))
    nb_path, f_path = folder / "notebook.jsonl", folder / "findings.md"
    notebook = [json.loads(x) for x in nb_path.read_text().splitlines() if x.strip()] if nb_path.exists() else []
    findings = f_path.read_text() if f_path.exists() else "(none yet)"

    def got(o):
        return o if len(o) <= 900 else o[:450] + "\n   ...\n" + o[-450:]

    def digest(limit=12000):
        s = "\n".join(f"{e['id']} [{e['match']:.1f}]{' ENTRY ' + e['entry'] if e.get('entry') else ''} Q: {e['question']}\n"
                      f"   expected: {e['expect'][:300]}\n   got: {got(e['out'])}" for e in notebook)
        if len(s) > limit:
            s = "...(earlier experiments omitted; see the findings and the map)\n" + s[-limit:]
        code = "\n\n".join(f"# {e['id']}\n{e['code'][:3500]}" for e in notebook[-3:])
        return s + (f"\n\n# Code of the most recent experiments\n```python\n{code}\n```" if code else "")

    t0 = time.time()
    for k in range(len(notebook) + 1, args.max_runs + 1):
        if args.hours and time.time() - t0 > args.hours * 3600:
            break
        ctx = f"# The task\n{task}\n\n# Findings\n{findings}\n\n# The map so far\n{mp.summary()}\n\n# Experiments so far\n{digest() or '(none)'}"
        r = llm(D_EXPERIMENTER, ctx, effort=args.effort, max_tokens=args.max_tokens)
        log_call(folder, k, "experimenter", r)
        code = code_block(r["text"])
        if code is None:
            continue
        q, exp = field(r["text"], "QUESTION"), (re.search(r"EXPECT:\s*(.+?)(?:\nENTRY:|```|$)", r["text"], re.S) or [None, ""])[1].strip()
        name = field(r["text"], "ENTRY")
        eid = f"E{k}"
        if name:
            box.run("reset()")
        out = box.run(code)
        e = {"id": eid, "question": q, "expect": exp, "code": code, "out": out[:6000], "audit": audit(code, "run")}
        if name:
            e["entry"] = name
            ef = box.dir / f"entry_{eid}.pt"
            if box.edits():
                shutil.copy(box.edits(), ef)
            box.run("reset()")
            mp.entries.append({"id": eid, "name": name, "depth": field(r["text"], "DEPTH").lower(),
                               "where": field(r["text"], "WHERE"), "mechanism": field(r["text"], "MECHANISM"),
                               "predict": parse_predict(field(r["text"], "PREDICT"), dev), "file": str(ef) if ef.exists() else None,
                               "changed": int(m.group(1)) if (m := re.search(r"\[(\d+) parameter tensors now differ", out)) else None})
            mp.save()
        j = llm(E_JUDGE, f"Expected:\n{exp}\n\nActual output:\n{out[:6000]}", effort="none", max_tokens=200)
        m = re.search(r"MATCH:\s*([01](?:\.\d+)?)", j["text"])
        e["match"] = float(m.group(1)) if m else 0.0
        notebook.append(e)
        with open(nb_path, "a") as fh:
            fh.write(json.dumps(e) + "\n")
        say(f"   {folder.name} {eid} match {e['match']:.1f}{' ENTRY ' + name if name else ''}: {q[:60]}")
        if e["match"] < 0.75:
            u = llm(D_UPDATER, f"# Findings\n{findings}\n\n# The surprising experiment\n{eid} Q: {q}\nexpected: {exp}\ngot: {got(out)}\n\n# The map\n{mp.summary()}",
                    effort=args.effort, max_tokens=args.max_tokens)
            log_call(folder, k, "updater", u)
            findings = u["text"].strip() or findings
        if k % 6 == 0:
            t = llm(D_THEORIST, f"# The task\n{task}\n\n# The verified map\n{mp.summary()}\n\n# The evidence\n{digest()}",
                    effort=args.effort, max_tokens=args.max_tokens)
            log_call(folder, k, "theorist", t)
            findings = t["text"].strip() or findings
        f_path.write_text(findings)
        if sum(bool("held_delta" not in x and x.get("file")) for x in mp.entries) >= args.verify_every:
            verify(box, mp, args.model, held, folder)
    verify(box, mp, args.model, held, folder)
    box.stop()
    print(report(folder))


def report(folder):
    folder = Path(folder)
    mp = Map(folder)
    nb = [json.loads(x) for x in (folder / "notebook.jsonl").read_text().splitlines() if x.strip()] if (folder / "notebook.jsonl").exists() else []
    done = [e for e in mp.entries if "held_delta" in e]
    ver = [e for e in done if e["verified"]]
    by_depth = {d: (sum(e["depth"] == d for e in ver), sum(e["depth"] == d for e in done)) for d in ("input", "output", "internal")}
    mechs = {(e["depth"], e["mechanism"].lower().strip()) for e in ver}
    curve, n = [], 0
    for x in nb:
        n += any(e["id"] == x["id"] and e.get("verified") for e in mp.entries)
        curve.append(n)
    lines = [f"# Discovery report: {folder}",
             f"- experiments: {len(nb)}; entries: {len(mp.entries)} ({len(done)} measured); verified: {len(ver)}",
             f"- yield: {len(ver) / max(len(nb), 1):.2f} verified entries per experiment",
             f"- verified by depth (verified / measured): {by_depth}",
             f"- distinct (depth, mechanism) among verified: {len(mechs)}",
             f"- thresholds: {json.dumps({b: round(t, 3) for b, t in (mp.thresholds() or {}).items()})}",
             f"- discovery curve (verified entries after each experiment): {curve}", "", "| id | depth | name | where | predicted | real effects (held-out) | verified |",
             "|---|---|---|---|---|---|---|"]
    for e in mp.entries:
        eff = ", ".join(f"{b} {v:+.2f}" for b, v in sorted(e.get("real_effects", {}).items(), key=lambda x: -abs(x[1]))[:6])
        lines.append(f"| {e['id']} | {e['depth']} | {e['name']} | {e['where'][:60]} | {e['predict']} | {eff} | {e.get('verified', 'pending')} |")
    (folder / "report.md").write_text("\n".join(lines) + "\n")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen3.5-0.8B")
    ap.add_argument("--out", default="runs/discover/test")
    ap.add_argument("--effort", default="high")
    ap.add_argument("--max-runs", type=int, default=40)
    ap.add_argument("--hours", type=float, default=0, help="stop after this many hours (0 = no limit)")
    ap.add_argument("--verify-every", type=int, default=8)
    ap.add_argument("--random", type=int, default=12, help="random interventions for the noise floor")
    ap.add_argument("--test-items", type=int, default=0, help="plumbing tests only: held-out questions per behaviour")
    ap.add_argument("--max-tokens", type=int, default=32000)
    ap.add_argument("--report")
    args = ap.parse_args()
    if args.report:
        print(report(args.report))
        return
    from probe.llm import LLM
    run(LLM(), args)


if __name__ == "__main__":
    main()

"""Capability removal by weight editing (docs/NORTH_STAR.md, docs/PLAN.md).

An editor changes a language model's weights directly so that it loses one named ability, and keeps the rest. Arms:
  unedited   the reference (just the grade)
  random     the scripted recipe below with a random direction (3 seeds): does any edit of that form do it?
  scripted   a fixed non-LLM recipe: the ability's direction = mean residual activation on the target's dev questions
             minus the mean on the control dev questions, at each layer; project it out of every matrix that writes to
             the residual stream; keep the layer whose edit best removes the dev target while keeping the dev controls
  mit        DeepSeek Flash, MIT's protocol: one conversation, one code block per turn
  helix      DeepSeek Flash inside Helix Probe: predict, run, judge, revise findings, theorist

    python bench/weights/edit.py --model Qwen/Qwen3.5-0.8B --ability gender --arm unedited
    python bench/weights/edit.py --model ... --ability gender --arm helix --reps 3
    python bench/weights/edit.py --report runs/edit

Grading (edit_grade.py) runs in a fresh process on the original model plus the saved edits, with held-out questions the
editor never sees. Thresholds are fixed in PLAN.md and in success() below.
"""
from __future__ import annotations

import argparse
import filecmp
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from bench.weights.edit_items import FLUENCY, abilities  # noqa: E402
from bench.weights.wsp import SYSTEM, audit, code_block, log_call, n_blocks, say  # noqa: E402

HERE = Path(__file__).resolve().parent


# =====================================================================================================  the box
class Box:
    """The model worker: one process holding the model, running the editor's code; edits saved after every run."""

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

        def reader():
            for line in self.p.stdout:            # skip anything that isn't the worker's JSON reply
                if line.startswith("{"):
                    try:
                        res.update(json.loads(line))
                        return
                    except json.JSONDecodeError:
                        pass
        t = threading.Thread(target=reader, daemon=True)
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
            out = (f"[timed out after {timeout} s; the session was restarted with your last saved edits]" if r is None
                   else "[the session crashed; it was restarted with your last saved edits]")
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


def spec_for(model, ab):
    sets = {"target": ab["target"], **ab["controls"], **{f"diag_{k}": v for k, v in ab["diag"].items()},
            **{f"post_{k}": v for k, v in ab.get("post", {}).items()}}   # post_*: added after the fact, never in the verdict
    return {"model": model, "sets": sets, "comeback": {"of": "target", "examples": ab["comeback_examples"]},
            "fluency": FLUENCY}


def grade(model, ab, folder, edits=None, name="grade.json"):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "grade_spec.json").write_text(json.dumps(spec_for(model, ab)))
    out = folder / name
    cmd = [sys.executable, str(HERE / "edit_grade.py"), str(folder / "grade_spec.json"), str(out)] + ([str(edits)] if edits else [])
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
    if p.returncode != 0:
        raise RuntimeError("grading failed:\n" + p.stderr[-3000:])
    return json.loads(out.read_text())


def baseline(model, name, ab, out_root):
    f = Path(out_root) / f"{model.split('/')[-1]}_{name}_unedited_r0" / "grade.json"
    if not f.exists():
        grade(model, ab, f.parent)
    return json.loads(f.read_text())


def verdict(g, b, ab):
    """The pre-registered thresholds (PLAN.md)."""
    t, t0 = g["scores"]["target"], b["scores"]["target"]
    ctrl = {k: (g["scores"][k], b["scores"][k]) for k in ab["controls"]}
    removed = t <= 0.2 * t0
    precise = all(v >= 0.9 * v0 for v, v0 in ctrl.values()) and g["ppl"] <= 1.25 * b["ppl"]
    durable = g.get("comeback", 1) <= 0.5 * b.get("comeback", 1)
    return {"present": t0 >= 0.8, "removed": removed, "precise": precise, "clean": removed and precise,
            "durable": removed and precise and durable}


# =====================================================================================================  the scripted arms
SCRIPTED = r'''
import torch
DEV_T = {dev_t!r}          # target dev questions with answers
DEV_C = {dev_c!r}          # control dev questions with answers
SEED = {seed!r}            # None = the ability's direction; an int = a random direction (control arm)
H = model.config.get_text_config().hidden_size
writers = [m for n, m in model.named_modules() if isinstance(m, torch.nn.Linear) and m.out_features == H and ".layers." in n]
emb = model.get_input_embeddings()

def project_out(d):
    d = (d / d.norm()).to(emb.weight.dtype).to(emb.weight.device)
    with torch.no_grad():
        for m in writers:
            m.weight -= torch.outer(d, d @ m.weight)
        emb.weight -= torch.outer(emb.weight @ d, d)

def dev_score():
    qt, at = zip(*DEV_T); qc, ac = zip(*DEV_C)
    t = sum(o.lower().strip(" .") == a.lower() for o, a in zip(ask(list(qt)), at)) / len(at)
    c = sum(o.lower().strip(" .") == a.lower() for o, a in zip(ask(list(qc)), ac)) / len(ac)
    return t, c

reset()
t0, c0 = dev_score()
R_t = resid([PRIMER + f"Q: {{q}}\nA:" for q, _ in DEV_T]).mean(1)
R_c = resid([PRIMER + f"Q: {{q}}\nA:" for q, _ in DEV_C]).mean(1)
if SEED is not None:
    g = torch.Generator().manual_seed(SEED)
    dirs = {{l: torch.randn(H, generator=g) for l in range(1, R_t.shape[0])}}
else:
    dirs = {{l: R_t[l] - R_c[l] for l in range(1, R_t.shape[0])}}
best = None
for l, d in dirs.items():
    reset(); project_out(d)
    t, c = dev_score()
    ok = c >= 0.9 * c0
    key = (not ok, t, -c)
    print(f"layer {{l}}: dev target {{t:.2f}} (was {{t0:.2f}}), dev controls {{c:.2f}} (was {{c0:.2f}})")
    if best is None or key < best[0]:
        best = (key, l)
reset(); project_out(dirs[best[1]])
print("chosen layer", best[1], "dev", dev_score())
'''


def run_scripted(box, ab, args, folder, seed=None):
    code = SCRIPTED.format(dev_t=[(q, a[0]) for q, a in ab["dev"]["target"]],
                           dev_c=[(q, a[0]) for q, a in ab["dev"]["controls"]], seed=seed)
    out = box.run(code, timeout=7200, max_out=60000)
    (folder / "scripted_log.txt").write_text(out)
    m = re.search(r"chosen layer (\d+)", out)
    if not m:
        raise RuntimeError("scripted edit failed:\n" + out[-3000:])
    return "", {"code_runs": 1, "layer": int(m.group(1))}


# =====================================================================================================  the LLM arms
def dev_text(ab):
    t = "\n".join(f"  {q} -> {a[0]}" for q, a in ab["dev"]["target"])
    c = "\n".join(f"  {q} -> {a[0]}" for q, a in ab["dev"]["controls"])
    return t, c


TASK = """You will change the weights of a language model so that {goal}

The model is {model} ({params:,} parameters), loaded with Hugging Face transformers. To run code, reply with exactly one code block that starts with ```python and ends with ```, and nothing else. We run it in a Python session that keeps the model in memory between runs, and reply with its printed output. Available in the session:
- model, tok: the model and its tokenizer (model.named_parameters(), model.named_modules() as usual)
- ask(questions, examples=None): the model's answers in the exact format used for grading (a short primer of unrelated questions, optional worked examples [(question, answer), ...], then "Q: <question>\\nA:"); PRIMER is that primer
- resid(prompts): residual-stream vectors at the last token, a tensor [layers + 1, len(prompts), hidden]
- generate(prompts, max_new_tokens=40), logprob(prompt, continuation), top_next(prompt, k=10)
- reset(): restore the original weights; changed(): the names of the parameters you have changed
- torch and np; your working directory is a folder kept between runs
Edits you make to the weights in memory persist between runs; nothing else does (forward hooks you register are removed after each run). The weights as they are when you finish are graded.

Rules: change the weights directly, with any arithmetic you choose (projections, rank-one updates, scaling, zeroing...). Do not train: no gradient descent on the weights (no .backward(), no optimizers). Computing activations and closed-form solutions is allowed. There is no internet access. Each run may take up to 600 seconds; its output is cut at 20,000 characters; you may run code up to {max_runs} times.

How you are graded: with ask(), on held-out questions you will not see. The ability to remove, as in these examples:
{dev_t}
must stop working. Abilities that must keep working, as in these examples:
{dev_c}
plus general knowledge and fluency on ordinary text, all measured against the original model. Removing the target while damaging these does not count. We also test whether the ability comes back when the question is preceded by a few worked examples.

When you are done, reply WITHOUT a code block: say what you changed and why it works."""

E_EXPERIMENTER = """You are changing a language model's weights to remove one ability while keeping the rest, one experiment at a time. You see the task, the current findings (claims about where the ability lives and what edits do, each citing the experiments behind it) and a digest of the experiments so far. Choose ONE experiment: locate where the ability lives, try or refine an edit, or check that the edit carries over to new questions and leaves the other abilities intact. Leave the model, at the end of each experiment, in the state you would want graded (call reset() first to start over). Write it as Python that PRINTS a short result. Before it runs, say what you expect it to print if the findings are right. Reply with exactly:
QUESTION: <one line>
EXPECT: <what the output should show, concretely>
```python
<code>
```
If the edit is done and checked, reply with only the word DONE."""
E_JUDGE = """You compare an expectation with an actual result. Reply with one line: MATCH: <a number from 0 to 1> <one short reason>. 1 = the result is what was expected; 0 = it contradicts it."""
E_UPDATER = """You maintain the findings for a weight-editing task: a short list of claims about where the ability lives and what edits do, each one line, each citing the experiments that support it, e.g. "- Projecting direction d out of layers 8-12 drops the target to 1/6 and keeps plurals [E4, E7]". An experiment just surprised the findings. Revise them so they agree with ALL the evidence: rewrite or remove the claims it contradicts and add what it shows. Evidence wins over any earlier claim. Keep the findings short. Reply with only the revised findings."""
E_THEORIST = """You see only the evidence from a weight-editing task (the experiments and their results), not anyone's current conclusions. Write the findings from scratch: a short list of one-line claims, each citing the experiments behind it, that explain the evidence: where the ability lives, which edits remove it, and what they break. Reply with only the findings."""
E_ANSWER = """Say what was changed in the model's weights and why it works, from the findings and the evidence. Be brief."""

# Helix variant 2 (arm "helix2", Nov 6): the same loop, with the evidence made complete for boxes whose experiments are
# code, and v3's goal-guess rule applied to a box whose deliverable is a state. Arm "helix" is unchanged.
#   1. The evidence shows the whole experiment: each result's head and tail (errors come at the end), and the code of
#      the most recent experiments (in FIND the experiment was its input, already shown; here it is code).
#   2. The experimenter states when it believes the model's state meets the goal (CANDIDATE); that state is saved; the
#      final role chooses, from the evidence, which candidate to deliver.
E_EXPERIMENTER_2 = E_EXPERIMENTER.replace("If the edit is done and checked,", """The digest shows the code of the most recent experiments: reuse what worked and fix what failed. If you believe this experiment will leave the model in a state that meets the goal (target broken, the other abilities kept), add the line CANDIDATE: yes before the code block; that state is saved, and you can keep experimenting. If the edit is done and checked,""")
E_ANSWER_2 = """Say what was changed in the model's weights and why it works, from the findings and the evidence. Be brief. Then, on the last line, choose which saved state to deliver for grading: DELIVER: <the id of the candidate experiment whose results best show the target broken and the other abilities kept>, or DELIVER: NONE to deliver the model as it is now. Candidates: {cands}."""


def task_text(ab, args, box):
    t, c = dev_text(ab)
    return TASK.format(goal=ab["goal"], model=args.model, params=box.info["params"], max_runs=args.max_runs, dev_t=t, dev_c=c)


def run_mit(llm, box, ab, args, folder):
    msgs = [{"role": "user", "content": task_text(ab, args, box)}]
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
        say(f"   {folder.name} run {runs}")
    return "", {"turns": args.max_turns, "code_runs": runs, "audit": flags, "extra_blocks": extra}


def run_helix(llm, box, ab, args, folder):
    v2 = args.arm == "helix2"
    taskmsg = task_text(ab, args, box)
    taskmsg = re.sub(r"To run code, reply with exactly one code block.*?with its printed output\. ", "", taskmsg, flags=re.S)
    taskmsg = taskmsg.split("\n\nWhen you are done")[0]
    findings, notebook = "(none yet)", []
    nb_path, f_path = folder / "notebook.jsonl", folder / "findings.md"
    if nb_path.exists():
        notebook = [json.loads(x) for x in nb_path.read_text().splitlines() if x.strip()]
        findings = f_path.read_text() if f_path.exists() else findings

    def got(o):
        return o if len(o) <= 900 else o[:450] + "\n   ...\n" + o[-450:]

    def digest(limit=14000):
        if not v2:
            s = "\n".join(f"{e['id']} [{e['match']:.1f}] Q: {e['question']}\n   expected: {e['expect'][:300]}\n   got: {e['out'][:900]}"
                          for e in notebook)
            return s if len(s) <= limit else "...(earlier experiments omitted; see the findings)\n" + s[-limit:]
        rows = [f"{e['id']} [{e['match']:.1f}]{' CANDIDATE' if e.get('candidate') else ''} Q: {e['question']}\n"
                f"   expected: {e['expect'][:300]}\n   got: {got(e['out'])}" for e in notebook]
        s = "\n".join(rows)
        if len(s) > limit:
            s = "...(earlier experiments omitted; see the findings)\n" + s[-limit:]
        code = "\n\n".join(f"# {e['id']}\n{e['code'][:3500]}" for e in notebook[-3:])
        return s + (f"\n\n# Code of the most recent experiments\n```python\n{code}\n```" if code else "")

    for k in range(len(notebook) + 1, args.max_runs + 1):
        r = llm(E_EXPERIMENTER_2 if v2 else E_EXPERIMENTER, f"# The task\n{taskmsg}\n\n# Findings\n{findings}\n\n# Experiments so far\n{digest() or '(none)'}",
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
        if v2 and re.search(r"CANDIDATE:\s*yes", r["text"], re.I):
            if box.edits():
                dst = box.dir / f"cand_{e['id']}.pt"
                prev = [box.dir / f"cand_{x['id']}.pt" for x in notebook if x.get("candidate")]
                prev = [f for f in prev if f.exists()]
                if prev and filecmp.cmp(prev[-1], box.edits(), shallow=False):
                    os.link(prev[-1], dst)            # same state as the last candidate: no second copy on disk
                else:
                    shutil.copy(box.edits(), dst)
            e["candidate"] = True
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
    cands = [e["id"] for e in notebook if e.get("candidate")]
    prompt = E_ANSWER_2.format(cands=", ".join(cands) or "none") if v2 else E_ANSWER
    a = llm(prompt, f"# The task\n{taskmsg}\n\n# Findings\n{findings}\n\n# Evidence\n{digest()}", effort=args.effort,
            max_tokens=args.max_tokens)
    log_call(folder, 0, "answer", a)
    delivered = None
    if v2:
        m = re.search(r"DELIVER:\s*(E\d+)", a["text"])
        if m and m.group(1) in cands:
            box.stop()
            src = box.dir / f"cand_{m.group(1)}.pt"
            if src.exists():
                shutil.copy(src, box.dir / "edits.pt")
            elif (box.dir / "edits.pt").exists():
                (box.dir / "edits.pt").unlink()       # the candidate state had no edits: deliver the original
            delivered = m.group(1)
    hits = [e["match"] for e in notebook]
    return a["text"], {"turns": len(notebook), "code_runs": len(notebook), "arrival": sum(hits) / len(hits) if hits else None,
                       "audit": [f"{e['id']}: {f}" for e in notebook for f in e["audit"]],
                       **({"candidates": cands, "delivered": delivered} if v2 else {})}


# =====================================================================================================  the job
def one(name, ab, rep, args, llm=None):
    tag = f"{args.model.split('/')[-1]}_{name}_{args.arm}" + (f"_{args.effort}" if args.arm in ("mit", "helix", "helix2") else "")
    folder = Path(args.out) / f"{tag}_r{rep}"
    if (folder / "result.json").exists():
        return json.loads((folder / "result.json").read_text())
    b = baseline(args.model, name, ab, args.out)
    if args.arm == "unedited":
        g, info, text = b, {"code_runs": 0}, ""
    else:
        folder.mkdir(parents=True, exist_ok=True)
        box = Box(folder, args.model, [str(ROOT), str(Path(args.out).resolve())])
        t0 = time.time()
        try:
            box.start()
            if args.arm in ("scripted", "random"):
                text, info = run_scripted(box, ab, args, folder, seed=None if args.arm == "scripted" else 1000 + rep)
            else:
                text, info = (run_mit if args.arm == "mit" else run_helix)(llm, box, ab, args, folder)   # helix2: run_helix, v2
        finally:
            box.stop()
        info["edit_seconds"] = round(time.time() - t0, 1)
        g = grade(args.model, ab, folder, box.edits())
        (folder / "answer.md").write_text(text)
    v = verdict(g, b, ab)
    post = {k: g["scores"].pop(k) for k in list(g["scores"]) if k.startswith("post_")}
    base_post = {k: b["scores"][k] for k in list(b["scores"]) if k.startswith("post_")}
    b = {**b, "scores": {k: x for k, x in b["scores"].items() if not k.startswith("post_")}}
    res = {"post": post, "base_post": base_post, "model": args.model, "ability": name, "arm": args.arm, "effort": args.effort, "rep": rep, **v,
           "scores": g["scores"], "comeback": g.get("comeback"), "ppl": g["ppl"], "base_scores": b["scores"],
           "base_comeback": b.get("comeback"), "base_ppl": b["ppl"], "changed_params": g["changed_params"],
           "changed_numel": g["changed_numel"], **info}
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "result.json").write_text(json.dumps(res, indent=1))
    say(f"== {tag} r{rep}: {'CLEAN' if v['clean'] else 'removed' if v['removed'] else 'not removed'}"
        f"{' DURABLE' if v['durable'] else ''} | target {g['scores']['target']} (base {b['scores']['target']}), "
        f"controls {[g['scores'][k] for k in ab['controls']]} (base {[b['scores'][k] for k in ab['controls']]}), "
        f"comeback {g.get('comeback')} (base {b.get('comeback')}), ppl {g['ppl']} (base {b['ppl']})")
    return res


def regrade(root, model):
    """Add the post-hoc measures to finished runs, without touching their results: grade the saved edits again into
    grade_post.json and add 'post' / 'base_post' to result.json (nothing else in it changes)."""
    abs_ = abilities()
    base_post = {}
    for f in sorted(Path(root).glob("*/result.json")):
        r = json.loads(f.read_text())
        if r["model"] != model or (r.get("post") and r.get("base_post")):
            continue
        ab, folder = abs_[r["ability"]], f.parent
        if r["ability"] not in base_post:
            bg = grade(model, ab, Path(root) / f"{model.split('/')[-1]}_{r['ability']}_unedited_r0", None, "grade_post.json")
            base_post[r["ability"]] = {k: v for k, v in bg["scores"].items() if k.startswith("post_")}
        if r["arm"] == "unedited":
            post = base_post[r["ability"]]
        elif r.get("post"):
            post = r["post"]                      # graded with the post-hoc sets already; only the base was missing
        else:
            edits = ROOT / "runs" / ".wsp" / hashlib.sha1(str(folder.resolve()).encode()).hexdigest()[:16] / "edits.pt"
            if not edits.exists():
                say(f"   {folder.name}: saved edits not found; not regraded")
                continue
            g = grade(model, ab, folder, edits, "grade_post.json")
            post = {k: v for k, v in g["scores"].items() if k.startswith("post_")}
        r["post"], r["base_post"] = post, base_post[r["ability"]]
        f.write_text(json.dumps(r, indent=1))
        say(f"   {folder.name}: post-hoc {post} (base {base_post[r['ability']]})")


def report(root):
    rows = {}
    for f in Path(root).glob("*/result.json"):
        r = json.loads(f.read_text())
        rows.setdefault((r["model"].split("/")[-1], r["ability"], r["arm"]), []).append(r)
    lines = ["| model | ability | arm | runs | clean | durable | target (base) | worst control vs base | comeback (base) | ppl (base) | reworded target, post-hoc (base) |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in sorted(rows):
        rs = sorted(rows[k], key=lambda r: r["rep"])
        worst = min(min(r["scores"][c] / max(r["base_scores"][c], 1e-9) for c in r["base_scores"]
                        if c != "target" and not c.startswith(("diag_", "post_"))) for r in rs)
        lines.append(f"| {k[0]} | {k[1]} | {k[2]} | {len(rs)} | {sum(r['clean'] for r in rs)} | {sum(r['durable'] for r in rs)} | "
                     f"{', '.join(str(r['scores']['target']) for r in rs)} ({rs[0]['base_scores']['target']}) | {worst:.2f} | "
                     f"{', '.join(str(r['comeback']) for r in rs)} ({rs[0]['base_comeback']}) | "
                     f"{', '.join(str(r['ppl']) for r in rs)} ({rs[0]['base_ppl']}) | "
                     f"{', '.join(str(r.get('post', {}).get('post_target_paraphrase', '–')) for r in rs)} "
                     f"({rs[0].get('base_post', {}).get('post_target_paraphrase', '–')}) |")
    Path(root, "report.md").write_text("\n".join(lines) + "\n")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen3.5-0.8B")
    ap.add_argument("--ability", default="gender,addition")
    ap.add_argument("--arm", choices=["unedited", "random", "scripted", "mit", "helix", "helix2"], default="unedited")
    ap.add_argument("--effort", default="high")
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--rep-start", type=int, default=0, help="first rep number (to split reps across machines)")
    ap.add_argument("--max-runs", type=int, default=40)
    ap.add_argument("--min-runs", type=int, default=8)
    ap.add_argument("--max-turns", type=int, default=80)
    ap.add_argument("--max-tokens", type=int, default=32000)
    ap.add_argument("--out", default="runs/edit")
    ap.add_argument("--report")
    ap.add_argument("--regrade", action="store_true", help="add the post-hoc measures to finished runs in --out")
    args = ap.parse_args()
    if args.report:
        print(report(args.report))
        return
    if args.regrade:
        regrade(args.out, args.model)
        print(report(args.out))
        return
    abs_ = abilities()
    llm = None
    if args.arm in ("mit", "helix", "helix2"):
        from probe.llm import LLM
        llm = LLM()
    for rep in range(args.rep_start, args.rep_start + args.reps):
        for name in args.ability.split(","):
            one(name, abs_[name], rep, args, llm)
    print(report(args.out))


if __name__ == "__main__":
    main()

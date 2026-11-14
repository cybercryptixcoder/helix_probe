"""Ask a specific question about a network that has a construction.

The lesson behind this (from reading runs on `main`): a reader asked "what does this network do" describes behaviour;
asked something specific ("which game is this?", "which inputs does it ignore?") it attributes that behaviour to an
answer. So after a construction exists, the owner can put a specific question to the reader. The reader gets the
delivered construction, the judge's report and its own final summary, and a python session over the weights to check
things before it answers (at most 8 steps). Every question and answer is saved in the run folder as questions.json.

Run:  python3 lab/ask.py <target id> <run id> "your question"
"""
import json, sys, time
from pathlib import Path

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB))
import constructor as C  # noqa: E402

SYSTEM = """You investigated a neural network and wrote a construction of it: a small program that computes what the network computes, through named variables that were tested against the network by interventions. The person who owns the network now has a specific question about it. Answer that question, specifically and directly.

Use what the construction and the judge's report establish. If the question needs something they do not establish, check it with the python tool first (W: the weights; X: the inputs the network is used on; run(x): outputs; acts(x): activations at every site; numpy as np). Say what your answer rests on: what was verified by the judge, what you just measured, and what is a guess. If the question asks you to choose or name something (a task, a game, a dataset, a rule), commit to one answer and give a confidence from 0 to 100. Keep the answer short: a few sentences or a short list."""

TOOLS = C.TOOLS[:1]


def ask(target, run_id, question, emit=None, max_steps=8):
    emit = emit or (lambda ev: None)
    rdir = C.OUT / target / run_id
    rec = json.loads((rdir / "run.json").read_text())
    cfg = rec["config"]
    cons = (rdir / "construction.py").read_text() if (rdir / "construction.py").exists() else "(no construction was delivered)"
    report = (rdir / "report.txt").read_text() if (rdir / "report.txt").exists() else "(no report)"
    user = (f"{rec['task']}\n\nYOUR CONSTRUCTION\n```python\n{cons}\n```\n\nTHE JUDGE'S REPORT ON IT\n{report}\n\n"
            f"YOUR FINAL SUMMARY\n{rec.get('final_message') or '(none)'}\n\nTHE QUESTION\n{question}")
    msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]
    kernel = C.Kernel(target, cfg["variant"], weights=cfg["weights"], seed=cfg.get("seed", 0))
    steps, answer, cost = [], "", 0.0
    try:
        for step in range(max_steps):
            last = step == max_steps - 1
            content, thinking, calls, usage, _ = C.chat(msgs, None if last else TOOLS, "high", 6000, emit, lambda: False)
            cost += C.luminal.cost(usage)
            if not calls:
                answer = content
                break
            msgs.append({"role": "assistant", "content": content, "reasoning_content": thinking, "tool_calls": calls})
            for c in calls:
                code = C.tool_code(c)
                emit({"type": "tool_call", "tool": "python", "code": code})
                res = kernel.run(code)
                emit({"type": "tool_result", "ok": res["ok"], "output": res["output"], "seconds": res["seconds"]})
                steps.append({"code": code, "output": res["output"]})
                note = "\n[this was your last check: answer the question now]" if step == max_steps - 2 else ""
                msgs.append({"role": "tool", "tool_call_id": c["id"], "content": (res["output"] or "(no output)") + note})
    finally:
        kernel.close()
    entry = {"asked": time.strftime("%Y-%m-%d %H:%M:%S"), "question": question, "answer": answer, "checks": steps, "cost": round(cost, 4)}
    f = rdir / "questions.json"
    hist = json.loads(f.read_text()) if f.exists() else []
    hist.append(entry)
    f.write_text(json.dumps(hist, indent=1))
    emit({"type": "answer", **entry})
    return entry


if __name__ == "__main__":
    e = ask(sys.argv[1], sys.argv[2], sys.argv[3])
    for s in e["checks"]:
        print("--- check ---\n" + s["code"] + "\n--- output ---\n" + s["output"][:1500])
    print("\nANSWER\n" + e["answer"] + f"\n\n(${e['cost']:.3f})")

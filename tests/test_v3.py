"""Offline checks of the pieces v3 adds (no LLM). Run: python -m tests.test_v3

1. hidden state: on the hidden-lock box, a model of the visible state alone can't fit the evidence; a model that
   replays the history can, and the loop keeps it.
2. trials: a fresh theory that predicts the future better replaces the current model after `trial` experiments;
   one that predicts worse doesn't.
3. the planner: with the true model, the very next step is a plan, and it opens the door.
4. budgets: a run stops when its cost budget is spent.
5. resuming a stateful box: a run stopped part-way and started again restores the box (by replaying its actions)
   and continues exactly where it was.
"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from envs.hidden_lock import HiddenLock  # noqa: E402
from probe.llm import ScriptedLLM  # noqa: E402
from probe.loop import Config, Run  # noqa: E402

TRUTH = '''def predict(probe):
    # replays the history to recover the hidden count
    count = 0
    for a in probe["history"]:
        count = 0 if a == "RESET" else count + (a == "A")
    door = probe["door"]
    steps = []
    for a in probe["actions"]:
        if a == "RESET":
            count, door = 0, "closed"
        elif a == "A":
            count += 1
        elif a == "B" and count == 3:
            door = "open"
        steps.append({"lamp": "on" if count >= 2 else "off", "door": door})
    return {"steps": steps}
'''
SCREEN_ONLY = '''def predict(probe):
    # uses only what is visible now: A turns the lamp on; B never opens the door
    lamp, steps = probe["lamp"], []
    for a in probe["actions"]:
        if a == "A":
            lamp = "on"
        if a == "RESET":
            lamp = "off"
        steps.append({"lamp": lamp, "door": probe["door"]})
    return {"steps": steps}
'''


class Scripted(ScriptedLLM):
    """Updater: offers the screen-only model. Theorist: offers `theory`."""

    def __init__(self, env, theory):
        super().__init__(env)
        self.theory = theory

    def __call__(self, system, user, temperature=0.7, effort="none", max_tokens=6000, messages=None):
        wrap = lambda c: {"text": f"```python\n{c}```\n", "usage": {}, "seconds": 0, "effort": effort, "attempts": 1}
        if "write a model from scratch" in user:
            return wrap(self.theory)
        if "revise the model" in user:
            return wrap(SCREEN_ONLY)
        return super().__call__(system, user, temperature, effort, max_tokens)


def run(folder, theory, **cfg):
    env = HiddenLock()
    log = []
    c = Config(**{"steps": 18, "theorist_every": 3, "trial": 2, "random_every": 1, "plan": False, **cfg})
    r = Run(env, folder, Scripted(env, theory), c, log=log.append)
    return r, r.go(), log


def main():
    with tempfile.TemporaryDirectory() as d:
        # 1 + 2: the screen-only fix is kept first; the true theory wins its trial and replaces it
        r, s, log = run(f"{d}/a", TRUTH)
        trials = [json.loads(l) for l in open(f"{d}/a/trials.jsonl")]
        assert any(t["won"] for t in trials), trials
        assert r.model.role == "theorist" and r.model.fit == 1.0, (r.model.role, r.model.fit)
        sc = r.score(SCREEN_ONLY)
        assert sc["fit"] < 1.0, "the screen-only model should not explain the hidden state"
        print(f"1. hidden state ok: the screen-only model fits {sc['fit']:.2f}; the history-replaying model fits 1.00")
        print(f"2. trials ok: the true theory won its trial ({trials[[t['won'] for t in trials].index(True)]['theirs']} "
              f"vs {trials[[t['won'] for t in trials].index(True)]['ours']}) and replaced the updater's model")

        # 2b: a wrong theory loses
        r2, _, _ = run(f"{d}/b", SCREEN_ONLY.replace('lamp = "on"', 'lamp = "off"'))
        t2 = [json.loads(l) for l in open(f"{d}/b/trials.jsonl")]
        assert t2 and not any(t["won"] for t in t2), t2
        print("   a wrong theory lost every trial")

        # 3: planner
        r3, s3, log3 = run(f"{d}/c", TRUTH, plan=True, steps=20)
        plans = [json.loads(l) for l in open(f"{d}/c/notebook.jsonl") if '"kind": "plan"' in l]
        assert r3.env.done() and plans and plans[-1]["observation"]["steps"][-1]["door"] == "open", plans[-1:]
        print(f"3. planner ok: once the model was right, the next step was a plan ({plans[-1]['probe']['actions']}) "
              "and it opened the door")

        # 4: budget
        r4, s4, log4 = run(f"{d}/e", TRUTH, budget=5, steps=50, theorist_every=0)
        assert s4["cost"] >= 5 and any("budget spent" in l for l in log4), (s4, log4[-3:])
        print(f"4. budget ok: stopped at cost {s4['cost']} (budget 5)")

        # 5: resume a stateful box
        env = HiddenLock()
        stop = {"n": 0}
        def should_stop():
            stop["n"] += 1
            return stop["n"] > 4
        c = Config(steps=10, theorist_every=0, random_every=1, plan=False)
        ra = Run(env, f"{d}/f", Scripted(env, TRUTH), c, log=lambda *_: None, should_stop=should_stop)
        assert ra.go() is None
        before = (env.count, env.door, list(env.history), len(ra.notebook))
        env2 = HiddenLock()
        rb = Run(env2, f"{d}/f", Scripted(env2, TRUTH), c, log=lambda *_: None)
        assert (env2.count, env2.door, env2.history, len(rb.notebook)) == before, ((env2.count, env2.door), before)
        rb.go()
        ids = [json.loads(l)["id"] for l in open(f"{d}/f/notebook.jsonl")]
        assert ids == [f"E{i + 1}" for i in range(len(ids))] and len(ids) == 10, ids
        print(f"5. resume ok: stopped after {before[3]} experiments, restored the hidden count {before[0]} by replay, "
              f"continued to {len(ids)}")


if __name__ == "__main__":
    main()

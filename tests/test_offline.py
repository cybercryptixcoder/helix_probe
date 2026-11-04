"""Offline checks of the mechanism (no LLM). Run: python -m tests.test_offline

1. Plumbing: random probes and a do-nothing model run end to end on both adapters.
2. Oracle: a stand-in experimenter that writes a wrong model first and the true rules second. The true model must be
   accepted (fit and held-out reach 100%), a model that fits worse must be rejected, and with the true model the
   free simulation must pick out a candidate that reaches a goal on the first real try.
"""
import inspect
import json
import random
import tempfile

from envs import knob_box, scrambled_grid
from probe.llm import ScriptedLLM
from probe.loop import Config, Run

GRID_TRUTH = inspect.getsource(scrambled_grid).split("class ScrambledGrid")[0].replace(
    "from probe.env import Environment, Task", "") + '''
def predict(probe):
    x, y = probe["start"]; path = []
    for b in probe["presses"]:
        x, y = step(x, y, b); path.append([x, y])
    return {"start": list(probe["start"]), "path": path}
'''
WRONG = "def predict(probe):\n    return {'start': probe['start'], 'path': []}\n"
WORSE = "def predict(probe):\n    return {}\n"


def route(s, t):
    prev, frontier = {s: None}, [s]
    while frontier:
        nxt = []
        for c in frontier:
            for b in "ABCDE":
                d = scrambled_grid.step(*c, b)
                if d not in prev:
                    prev[d] = (c, b); nxt.append(d)
        frontier = nxt
    out = ""
    while prev[t]:
        t, b = prev[t]; out = b + out
    return out


class Oracle(ScriptedLLM):
    """revise #1 -> a partly right model, #2 -> a worse one (must be rejected), then the truth."""

    def __init__(self, env):
        super().__init__(env)
        self.revisions = 0

    def __call__(self, system, user, temperature=0.7):
        if "reach a goal" in user:
            # decoys first, a correct sequence last: only the simulation can tell which one works
            start = json.loads(user.split("Your probe's start must be ")[1].split(";")[0])
            target = tuple(json.loads(user.split("ends on ")[1].split(".")[0]))
            cands = [{"start": start, "presses": "".join(random.choice("ABCDE") for _ in range(6))} for _ in range(20)]
            cands.append({"start": start, "presses": route(tuple(start), target)})
            return {"text": "```json\n" + json.dumps({"question": "search", "candidates": cands}) + "\n```"}
        if "update your model" in user:
            self.revisions += 1
            code = {1: WRONG, 2: WORSE}.get(self.revisions, GRID_TRUTH)
            return {"text": '```json\n{"beliefs": ["b"], "notes": "n"}\n```\n```python\n' + code + "```"}
        return super().__call__(system, user, temperature)


def main():
    with tempfile.TemporaryDirectory() as d:
        for mod, cls in ((scrambled_grid, scrambled_grid.ScrambledGrid), (knob_box, knob_box.KnobBox)):
            env = cls()
            Run(env, f"{d}/{env.name}", ScriptedLLM(env), Config(steps=5, tasks=1), log=lambda *_: None).go()
        print("1. plumbing ok")

        env = scrambled_grid.ScrambledGrid()
        llm = Oracle(env)
        log = []
        run = Run(env, f"{d}/oracle", llm, Config(steps=6, tasks=3, tries=1, candidates=21, retries=1), log=log.append)
        s = run.go()
        assert any("rejected" in l for l in log), "a worse model was not rejected"
        assert s["fit"] == 1.0 and s["heldout"] == 1.0, s
        assert s["goals"]["reached"] == 3, s["goals"]
        print(f"2. oracle ok: fit {s['fit']:.0%}, held-out {s['heldout']:.0%}, goals {s['goals']['reached']}/3 "
              f"first try, model v{s['model_version']}")


if __name__ == "__main__":
    main()

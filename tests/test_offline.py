"""Offline checks of every piece of v2 (no LLM). Run: python -m tests.test_offline

1. plumbing: both toy boxes and both FIND boxes run end to end with a scripted stand-in.
2. the accept rule: a model that memorises the notebook (fit 100%) loses to a general one on the sealed exam, even
   when the general one fits the notebook worse; a tie on both goes to the shorter model.
3. the roles: the theorist's prompt never contains the current model; the updater's always does; the theorist runs
   on schedule and after the updater stalls.
4. the true model: accepted, exam and held-out perfect, early stop fires, goals reached on the first real try.
5. FIND: true functions score 1 under the official scorer (except those whose corrupted interval is fresh noise),
   an empty model scores 0, and the string truth pairs come from the real functions.
"""
import inspect
import json
import random
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from envs import scrambled_grid  # noqa: E402
from envs.find_numeric import FindNumeric  # noqa: E402
from envs.find_strings import FindStrings  # noqa: E402
from envs.knob_box import KnobBox  # noqa: E402
from probe.llm import ScriptedLLM  # noqa: E402
from probe.loop import Config, Run  # noqa: E402

GRID_TRUTH = inspect.getsource(scrambled_grid).split("class ScrambledGrid")[0].replace(
    "from probe.env import Environment, Task", "") + '''
def predict(probe):
    # the true rules
    x, y = probe["start"]; path = []
    for b in probe["presses"]:
        x, y = step(x, y, b); path.append([x, y])
    return {"start": list(probe["start"]), "path": path}
'''


PARTIAL = GRID_TRUTH.replace('"A": (0, 1, 1)', '"A": (0, 1, 2)')   # general, but A is wrong: exam well above 0


def lookup_model(entries):
    """Memorises the notebook exactly; predicts nothing else."""
    table = {json.dumps(e["probe"], sort_keys=True): e["observation"] for e in entries}
    return f"import json\nT = {json.dumps(table)!r}\ndef predict(probe):\n    return json.loads(T).get(json.dumps(probe, sort_keys=True), {{}})\n"


class Recorder(ScriptedLLM):
    """Scripted roles. The updater first offers a partly right general model, then only lookup tables of the notebook
    (which fit it perfectly). The theorist offers the truth. Every prompt is recorded so the tests can check what each role saw."""

    def __init__(self, env, run_ref):
        super().__init__(env)
        self.run_ref, self.seen = run_ref, []

    def __call__(self, system, user, temperature=0.7, effort="none", max_tokens=6000):
        role = "theorist" if "write a model from scratch" in user else "updater" if "revise the model" in user else "other"
        self.seen.append((role, user))
        if role == "updater":
            n = sum(1 for r, _ in self.seen if r == "updater")
            code = PARTIAL if n == 1 else lookup_model(self.run_ref[0].notebook.entries)
            return {"text": f"```python\n{code}```\nchanged", "usage": {}, "seconds": 0, "effort": effort, "attempts": 1}
        if role == "theorist":
            return {"text": f"```python\n{GRID_TRUTH}```\nidea", "usage": {}, "seconds": 0, "effort": effort, "attempts": 1}
        if "reach a goal" in user:
            start = json.loads(re.search(r"start must be (\[[^\]]*\])", user).group(1))
            target = tuple(json.loads(re.search(r"ends on (\[[^\]]*\])", user).group(1)))
            cands = [{"start": start, "presses": "".join(random.choice("ABCDE") for _ in range(6))} for _ in range(4)]
            cands.append({"start": start, "presses": route(tuple(start), target)})
            return {"text": "```json\n" + json.dumps({"question": "search", "candidates": cands}) + "\n```",
                    "usage": {}, "seconds": 0, "effort": effort, "attempts": 1}
        return super().__call__(system, user, temperature, effort, max_tokens)


def route(s, t):
    prev, frontier = {s: None}, [s]
    while frontier:
        nxt = []
        for c in frontier:
            for b in "ABCDE":
                d = scrambled_grid.step(*c, b)
                if d not in prev:
                    prev[d] = (c, b)
                    nxt.append(d)
        frontier = nxt
    out = ""
    while prev[t]:
        t, b = prev[t]
        out = b + out
    return out


def main():
    quiet = lambda *_: None
    with tempfile.TemporaryDirectory() as d:
        # 1. plumbing
        for env in (scrambled_grid.ScrambledGrid(), KnobBox(), FindNumeric("f00030"), FindStrings("f00019")):
            Run(env, f"{d}/{env.name}", ScriptedLLM(env), Config(steps=4, tasks=1 if env.make_tasks(random.Random(0), 1) else 0),
                log=quiet).go()
        print("1. plumbing ok (grid, knob, FIND numeric, FIND strings)")

        # 2. the accept rule, directly
        env = scrambled_grid.ScrambledGrid()
        run = Run(env, f"{d}/rule", ScriptedLLM(env), Config(steps=0, exam=8), log=quiet)
        for _ in range(12):
            p = env.random_probe(run.rng)
            run.run_experiment("learn", "q", p)
        lookup = run.score(lookup_model(run.notebook.entries))
        truth = run.score(GRID_TRUTH)
        assert lookup["fit"] == 1.0 and lookup["exam"] < 0.5, lookup
        assert truth["exam"] == 1.0
        assert Run.better(truth, lookup)[0] and not Run.better(lookup, truth)[0]
        partial = dict(truth, fit=0.9)                       # generalises better but fits the notebook worse
        assert Run.better(partial, lookup)[0], "exam must come before fit"
        assert Run.better(dict(truth, size=10), truth)[0] and not Run.better(truth, dict(truth, size=10))[0]
        print(f"2. accept rule ok: a lookup table (fit {lookup['fit']:.0%}, exam {lookup['exam']:.0%}) loses to the "
              f"true rules (exam {truth['exam']:.0%}); exam beats fit; ties go to the shorter model")

        # 3 + 4. the roles and the true model, through the loop
        ref = [None]
        llm = Recorder(env, ref)
        log = []
        run = Run(env, f"{d}/roles", llm, Config(steps=30, exam=6, theorist_every=0, theorist_on_stall=2,
                                                 stop_after=4, tasks=3, tries=1, candidates=5), log=log.append)
        ref[0] = run
        s = run.go()
        th = [u for r, u in llm.seen if r == "theorist"]
        up = [u for r, u in llm.seen if r == "updater"]
        assert th, "the theorist never ran (it should after the updater stalls)"
        assert all("def predict" not in u.split("# Your job")[0] for u in th), "the theorist saw a model"
        assert all("# The current model" in u for u in up), "the updater didn't see the model"
        assert any("not kept" in l for l in log), "the lookup tables were never rejected"
        assert not any("by the updater: exam 0.00" in l for l in log), "a lookup table was kept"
        assert any("stopping early" in l for l in log), "early stop never fired"
        assert s["exam"] == 1.0 and s["heldout"] == 1.0, s
        assert s["goals"]["reached"] == 3 and s["goals"]["tries_used"] == [1, 1, 1], s["goals"]
        print(f"3. roles ok: the theorist ran {len(th)}x without seeing any model; updater lookups rejected "
              f"{sum('not kept' in l for l in log)}x")
        print(f"4. true model ok: kept as v{s['model_version']} by the {s['model_role']}, exam 100%, held-out 100%, "
              f"stopped after {s['experiments'] - 3} experiments, goals 3/3 on the first try")

    # 5. FIND scoring
    from bench.find.score import score, strings_truth
    sample = json.loads((ROOT / "bench/find/data/sample.json").read_text())
    solved, noisy = 0, 0
    for fid in sample["numeric"]:
        info = json.loads((ROOT / f"bench/find/data/numeric/{fid}/info.json").read_text())
        if info["kind"] == "mlp":
            continue
        code = (ROOT / f"bench/find/data/numeric/{fid}/function_code.py").read_text() + \
            '\ndef predict(probe):\n    return {"y": [float(function(x)) for x in probe["x"]]}\n'
        r = score("numeric", fid, code)
        solved += r["score"]
        noisy += r["score"] == 0 and "np.random" in code
    n_code = sum(1 for f in sample["numeric"]
                 if json.loads((ROOT / f"bench/find/data/numeric/{f}/info.json").read_text())["kind"] == "code")
    assert solved + noisy == n_code, (solved, noisy, n_code)
    assert score("strings", sample["strings"][0], "def predict(probe):\n    return {}\n")["score"] == 0
    env = FindStrings(sample["strings"][0])
    assert all(env.probe({"inputs": [i]})["outputs"][0] == o for i, o in strings_truth(sample["strings"][0]))
    print(f"5. FIND scoring ok: true numeric functions solve {int(solved)}/{n_code} (the other {noisy} return fresh "
          "noise in their corrupted interval); empty models score 0; string truth pairs reproduce")


if __name__ == "__main__":
    main()

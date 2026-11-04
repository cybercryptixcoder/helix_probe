"""Run Helix Probe arms on FIND functions, then score every model version with FIND's official metric.

    python bench/find/run.py --out results/find/x --arms v2 v1 v2-random --steps 25 --workers 4
    python bench/find/run.py --out runs/dev --data bench/find/dev --arms v2 v2-no-theorist --limit 4

One function = one independent run with a fresh memory. Runs share one LLM client, so all model calls together
start at most once a second (Luminal's long-run rate per key). Finished runs are skipped and unfinished ones resume,
so the same command continues an interrupted job; a bigger --steps extends finished v2 runs that didn't stop early.
"""
from __future__ import annotations

import argparse
import json
import signal
import sys
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "versions" / "v1"))

from bench.find.curve import curve  # noqa: E402
from envs.find_numeric import FindNumeric  # noqa: E402
from envs.find_strings import FindStrings  # noqa: E402
from probe.llm import LLM, ScriptedLLM  # noqa: E402

# Each arm: which engine, and what differs from the default configuration.
ARMS = {
    "v2": ("v2", {}),                                   # the system: mixed experiments, theorist, exam
    "v2-directed": ("v2", {"random_every": 0}),          # every experiment chosen by the experimenter
    "v2-no-theorist": ("v2", {"theorist_every": 0, "theorist_on_stall": 0}),
    "v2-no-exam": ("v2", {"exam": 0}),
    "v2-random": ("v2", {"experimenter": "random"}),
    "v2-theorist-low": ("v2", {"effort": {"experimenter": "none", "updater": "none", "theorist": "low"}}),
    "v1": ("v1", {}),
}
_print = threading.Lock()
STOP = threading.Event()        # set by a stop signal: runs finish their current step, nothing new starts


def say(msg):
    with _print:
        print(time.strftime("%H:%M:%S"), msg, flush=True)


def trim_jsonl(path: Path):
    """Drop a last line torn by a kill (v1, frozen, can't read one)."""
    if not path.exists():
        return
    good = []
    for line in path.read_text().splitlines():
        try:
            json.loads(line)
            good.append(line)
        except json.JSONDecodeError:
            break
    path.write_text("".join(l + "\n" for l in good))


def make_env(cat, fid, data):
    return (FindNumeric if cat == "numeric" else FindStrings)(fid=fid, data=str(ROOT / data))


def one(arm, cat, fid, args, llm):
    folder = Path(args.out) / arm / f"{cat}_{fid}"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "bench.json").write_text(json.dumps({"arm": arm, "category": cat, "fid": fid, "data": args.data,
                                                   "steps": args.steps}))
    env = make_env(cat, fid, args.data)
    log_file = (folder / "run.log").open("a")

    def log(m):
        log_file.write(m + "\n")
        log_file.flush()

    engine, over = ARMS[arm]
    t0 = time.time()
    if engine == "v1":
        from probe_v1.loop import Config as C1, Run as R1
        for name in ("notebook.jsonl", "calls.jsonl"):
            trim_jsonl(folder / name)
        done = sum(1 for l in (folder / "notebook.jsonl").open() if '"kind": "learn"' in l) \
            if (folder / "notebook.jsonl").exists() else 0
        run = R1(env, folder, llm, C1(steps=max(0, args.steps - done), heldout=100, seed=args.seed), log=log)
        if args.steps - done > 0 or not (folder / "summary.json").exists():
            run.go()        # v1 has no stop hook: a stop signal lets its run finish
    else:
        from probe.loop import Config, Run
        cfg = Config(steps=args.steps, exam=args.exam, seed=args.seed, heldout=100)
        for k, v in over.items():
            setattr(cfg, k, v)
        if Run(env, folder, llm, cfg, log=log, should_stop=STOP.is_set).go() is None:
            log_file.close()
            return None
    log_file.close()
    c = curve(folder)
    s = json.loads((folder / "summary.json").read_text())
    say(f"== done {arm} {cat} {fid}: official {c['final']:.2f}, {s['experiments']} experiments, "
        f"{s['llm_calls']} calls, {time.time() - t0:.0f} s")
    return c


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--out", required=True)
    a.add_argument("--data", default=str(ROOT / "bench" / "find" / "data"))
    a.add_argument("--arms", nargs="+", default=["v2"], choices=sorted(ARMS))
    a.add_argument("--categories", nargs="+", default=["numeric", "strings"])
    a.add_argument("--limit", type=int, default=0, help="first N functions per category (0 = all)")
    a.add_argument("--steps", type=int, default=25)
    a.add_argument("--exam", type=int, default=4)
    a.add_argument("--workers", type=int, default=4)
    a.add_argument("--seed", type=int, default=0)
    a.add_argument("--fake", action="store_true", help="no model: crash test only")
    args = a.parse_args()
    data = Path(args.data).resolve()
    args.data = str(data.relative_to(ROOT)) if data.is_relative_to(ROOT) else str(data)   # portable across machines
    sample = json.loads((ROOT / args.data / "sample.json").read_text())
    jobs = [(arm, cat, fid) for cat in args.categories for fid in (sample[cat][:args.limit] if args.limit else sample[cat])
            for arm in args.arms]
    Path(args.out).mkdir(parents=True, exist_ok=True)
    (Path(args.out) / "job.json").write_text(json.dumps(vars(args), indent=1))
    say(f"== {len(jobs)} runs: arms {args.arms}, {args.steps} steps each, {args.workers} at a time")

    if args.fake:
        llm_for = lambda arm, cat, fid: ScriptedLLM(make_env(cat, fid, args.data))
    else:
        shared = LLM()
        llm_for = lambda arm, cat, fid: shared
    def on_stop(*_):
        if not STOP.is_set():
            say("== stop requested: runs finish the step in progress and save; nothing new starts")
        STOP.set()
    signal.signal(signal.SIGTERM, on_stop)
    signal.signal(signal.SIGINT, on_stop)
    failed = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        def guarded(arm, cat, fid):
            return None if STOP.is_set() else one(arm, cat, fid, args, llm_for(arm, cat, fid))
        futs = {pool.submit(guarded, arm, cat, fid): (arm, cat, fid) for arm, cat, fid in jobs}
        for f in as_completed(futs):
            try:
                f.result()
            except Exception:
                failed += 1
                say(f"(run failed: {futs[f]})\n" + traceback.format_exc()[-1500:])
    if STOP.is_set():
        say("== stopped cleanly; run the same command again to continue")
        return 75
    say(f"== all runs finished ({failed} failed)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

"""Run Helix Probe on ARC-AGI-3 public games and score each with the toolkit's official calculator.

    python bench/arc/run.py --out runs/arc/arc-v3 --games all --budget-x 3 --workers 8
    python bench/arc/run.py --out runs/arc/dev --games ls20 ft09 --steps 40

One game = one run with a fresh memory, played in stateful mode (the game keeps running; every action counts,
resets included). The budget per game is --budget-x times the human baseline actions for that game (the sum over
its levels), so a hard game gets more actions, and a run stops when its game is won, its budget is spent, or
--steps experiments are done. Finished runs are skipped and unfinished ones resume from their notebook (the game
is restored by replaying its actions), so the same command continues an interrupted job. A stop signal lets every
run finish the step in progress and save; exit code 75 means "stopped, run again to continue".

Score: per game, the toolkit's EnvironmentScoreCalculator (RHAE: per level min(115, (human/agent actions)^2 x 100),
weighted by level index); the job score is the mean over games, as ARC Prize reports it.
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

from probe.llm import LLM, ScriptedLLM, load_dotenv  # noqa: E402
from probe.loop import Config, Run  # noqa: E402

ARMS = {
    "v3": {},                                    # the current system
    "v3-no-plan": {"plan": False},               # no planner: every experiment chosen by the experimenter
    "v3-random": {"experimenter": "random", "plan": False},   # random actions only (a floor)
}
_print = threading.Lock()
STOP = threading.Event()


def say(msg):
    with _print:
        print(time.strftime("%H:%M:%S"), msg, flush=True)


def all_games():
    import os
    from arc_agi import Arcade
    a = Arcade(arc_api_key=os.environ.get("ARC_API_KEY", ""), environments_dir=str(ROOT / "bench" / "arc" / "games"))
    return {e.game_id: sum(e.baseline_actions) for e in a.get_environments()}


def one(arm, game, base, args, llm):
    from envs.arc_agi3 import ArcAgi3
    folder = Path(args.out) / arm / game.split("-")[0]
    folder.mkdir(parents=True, exist_ok=True)
    budget = int(args.budget_x * base)
    (folder / "bench.json").write_text(json.dumps({"arm": arm, "game": game, "baseline": base, "budget": budget,
                                                   "steps": args.steps, "max_actions": args.max_actions}))
    env = ArcAgi3(game=game, max_actions=str(args.max_actions))
    log_file = (folder / "run.log").open("a")

    def log(m):
        log_file.write(m + "\n")
        log_file.flush()

    cfg = Config(steps=args.steps, budget=budget, seed=args.seed, heldout=0)
    for k, v in ARMS[arm].items():
        setattr(cfg, k, v)
    t0 = time.time()
    out = Run(env, folder, llm, cfg, log=log, should_stop=STOP.is_set).go()
    log_file.close()
    if out is None:
        return None
    s = json.loads((folder / "summary.json").read_text())
    b = s.get("box_score") or {}
    say(f"== done {arm} {game}: score {b.get('score', 0):.2f}, levels {b.get('levels_completed')}/{b.get('levels')}, "
        f"{b.get('actions')} actions (human {base}), {s['llm_calls']} calls, {time.time() - t0:.0f} s")
    return s


def report(out):
    out = Path(out)
    rows = {}
    for f in sorted(out.glob("*/*/summary.json")):
        s = json.loads(f.read_text())
        b = s.get("box_score") or {}
        rows.setdefault(f.parent.parent.name, []).append((f.parent.name, b, s))
    lines = ["# ARC-AGI-3 results", "", "| Arm | games | mean score | levels | actions | human actions | calls |",
             "|---|---|---|---|---|---|---|"]
    js = {}
    for arm, rs in rows.items():
        n = len(rs)
        mean = sum(b.get("score", 0) for _, b, _ in rs) / n
        lv = sum(b.get("levels_completed", 0) for _, b, _ in rs)
        lt = sum(b.get("levels", 0) for _, b, _ in rs)
        acts = sum(b.get("actions", 0) for _, b, _ in rs)
        hum = sum(sum(b.get("baseline", [])) for _, b, _ in rs)
        calls = sum(s.get("llm_calls", 0) for _, _, s in rs)
        lines.append(f"| {arm} | {n} | {mean:.2f} | {lv}/{lt} | {acts} | {hum} | {calls} |")
        js[arm] = {"games": n, "mean_score": mean, "levels": [lv, lt], "actions": acts, "human_actions": hum,
                   "calls": calls, "per_game": {g: b for g, b, _ in rs}}
    lines += ["", "Per game:", "", "| Arm | game | score | levels | actions | human |", "|---|---|---|---|---|---|"]
    for arm, rs in rows.items():
        for g, b, _ in rs:
            lines.append(f"| {arm} | {g} | {b.get('score', 0):.2f} | {b.get('levels_completed')}/{b.get('levels')} | "
                         f"{b.get('actions')} | {sum(b.get('baseline', []))} |")
    (out / "report.md").write_text("\n".join(lines) + "\n")
    (out / "report.json").write_text(json.dumps(js, indent=1))
    return "\n".join(lines[:4 + len(rows)])


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--out", required=True)
    a.add_argument("--arms", nargs="+", default=["v3"], choices=sorted(ARMS))
    a.add_argument("--games", nargs="+", default=["all"], help="'all' or game id prefixes like ls20 ft09")
    a.add_argument("--budget-x", type=float, default=3.0, help="action budget per game, in human baselines")
    a.add_argument("--steps", type=int, default=400, help="most experiments per game")
    a.add_argument("--max-actions", type=int, default=8, help="most actions in one experiment")
    a.add_argument("--workers", type=int, default=8)
    a.add_argument("--seed", type=int, default=0)
    a.add_argument("--fake", action="store_true", help="no model: crash test only")
    a.add_argument("--report", action="store_true", help="only write the report")
    args = a.parse_args()
    if args.report:
        print(report(args.out))
        return 0
    load_dotenv(str(ROOT / ".env"))       # ARC_API_KEY (the toolkit downloads each game once)
    games = all_games()
    if args.games != ["all"]:
        games = {g: b for g, b in games.items() if g.split("-")[0] in args.games or g in args.games}
    jobs = [(arm, g, b) for g, b in sorted(games.items()) for arm in args.arms]
    Path(args.out).mkdir(parents=True, exist_ok=True)
    (Path(args.out) / "job.json").write_text(json.dumps(vars(args), indent=1))
    say(f"== {len(jobs)} runs: arms {args.arms}, budget {args.budget_x}x human actions, {args.workers} at a time")
    shared = None if args.fake else LLM()

    def on_stop(*_):
        if not STOP.is_set():
            say("== stop requested: runs finish the step in progress and save; nothing new starts")
        STOP.set()
    signal.signal(signal.SIGTERM, on_stop)
    signal.signal(signal.SIGINT, on_stop)
    failed = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        def guarded(arm, g, b):
            if STOP.is_set():
                return None
            llm = shared
            if args.fake:
                from envs.arc_agi3 import ArcAgi3
                llm = ScriptedLLM(ArcAgi3(game=g))
            return one(arm, g, b, args, llm)   # a finished run returns at once (its game is restored by replay)
        futs = {pool.submit(guarded, *j): j for j in jobs}
        for f in as_completed(futs):
            try:
                f.result()
            except Exception:
                failed += 1
                say(f"(run failed: {futs[f][:2]})\n" + traceback.format_exc()[-1500:])
    print(report(args.out))
    if STOP.is_set():
        say("== stopped cleanly; run the same command again to continue")
        return 75
    say(f"== all runs finished ({failed} failed)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

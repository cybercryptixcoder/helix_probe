"""python -m probe.run <adapter.py> [options]

    python -m probe.run envs/scrambled_grid.py --steps 30 --tasks 5
    python -m probe.run envs/find_strings.py --env-arg fid=f00012 --steps 25
    python -m probe.run envs/knob_box.py --offline --steps 3           # no model: crash test only

--steps is the TOTAL number of learn steps: run the same command with the same --out and a bigger --steps to
continue a run.
"""
from __future__ import annotations

import argparse
import importlib.util
import inspect
import time
from pathlib import Path

from probe.env import Environment
from probe.llm import LLM, ScriptedLLM
from probe.loop import Config, Run


def load_env(path, kwargs=None):
    spec = importlib.util.spec_from_file_location(Path(path).stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    found = [c for _, c in inspect.getmembers(mod, inspect.isclass)
             if issubclass(c, Environment) and c is not Environment and c.__module__ == mod.__name__]
    if len(found) != 1:
        raise SystemExit(f"{path} must define exactly one Environment subclass (found {len(found)})")
    return found[0](**(kwargs or {}))


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("adapter", help="path to an adapter file (one Environment subclass)")
    a.add_argument("--env-arg", nargs="*", default=[], help="key=value passed to the adapter's constructor")
    a.add_argument("--steps", type=int, default=30, help="most experiments in the run (total)")
    a.add_argument("--budget", type=float, default=0, help="most total cost in the box's units (0 = no limit)")
    a.add_argument("--exam", type=int, default=0, help="sealed exam probes (0 = none; judge by trials)")
    a.add_argument("--trial", type=int, default=3, help="experiments a new theory is tried on")
    a.add_argument("--no-plan", action="store_true", help="don't use the planner")
    a.add_argument("--theorist-every", type=int, default=6, help="learn steps between theorist calls (0 = never)")
    a.add_argument("--experimenter", choices=["llm", "random"], default="llm")
    a.add_argument("--random-every", type=int, default=2, help="every k-th experiment is a random probe (0 = never)")
    a.add_argument("--effort", nargs="*", default=[], help="role=level, e.g. theorist=low")
    a.add_argument("--tasks", type=int, default=0, help="goals to attempt after learning")
    a.add_argument("--tries", type=int, default=3, help="real attempts per goal")
    a.add_argument("--knowledge", nargs="*", default=[], help="markdown files added to the library")
    a.add_argument("--no-env-knowledge", action="store_true", help="ignore the adapter's own knowledge text")
    a.add_argument("--out", default=None)
    a.add_argument("--seed", type=int, default=0)
    a.add_argument("--offline", action="store_true", help="no model: random probes, to test the plumbing")
    args = a.parse_args()

    env = load_env(args.adapter, dict(kv.split("=", 1) for kv in args.env_arg))
    if args.no_env_knowledge:
        env.knowledge = ""
    cfg = Config(steps=args.steps, budget=args.budget, exam=args.exam, trial=args.trial, plan=not args.no_plan,
                 theorist_every=args.theorist_every,
                 experimenter=args.experimenter, random_every=args.random_every, tasks=args.tasks, tries=args.tries, seed=args.seed)
    for kv in args.effort:
        role, level = kv.split("=", 1)
        cfg.effort[role] = level
    out = args.out or f"runs/{env.name}-{time.strftime('%Y%m%d-%H%M%S')}"
    llm = ScriptedLLM(env, args.seed) if args.offline else LLM()
    Run(env, out, llm, cfg, knowledge_files=args.knowledge).go()
    print(f"run folder: {out}")


if __name__ == "__main__":
    main()

"""python -m probe.run envs/scrambled_grid.py --steps 40 --tasks 5 [--out runs/x] [--knowledge hints.md] [--offline]

Running the same command again with the same --out continues the run where it stopped.
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


def load_env(path):
    spec = importlib.util.spec_from_file_location(Path(path).stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    found = [c for _, c in inspect.getmembers(mod, inspect.isclass)
             if issubclass(c, Environment) and c is not Environment and c.__module__ == mod.__name__]
    if len(found) != 1:
        raise SystemExit(f"{path} must define exactly one Environment subclass (found {len(found)})")
    return found[0]()


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("adapter", help="path to an adapter file (one Environment subclass)")
    a.add_argument("--steps", type=int, default=30, help="learn steps (one experiment each)")
    a.add_argument("--tasks", type=int, default=0, help="goals to attempt after learning")
    a.add_argument("--tries", type=int, default=3, help="real attempts per goal")
    a.add_argument("--knowledge", nargs="*", default=[], help="markdown files added to the library")
    a.add_argument("--no-env-knowledge", action="store_true", help="ignore the adapter's own knowledge text")
    a.add_argument("--out", default=None)
    a.add_argument("--seed", type=int, default=0)
    a.add_argument("--offline", action="store_true", help="no model: random probes, to test the plumbing")
    args = a.parse_args()

    env = load_env(args.adapter)
    if args.no_env_knowledge:
        env.knowledge = ""
    out = args.out or f"runs/{env.name}-{time.strftime('%Y%m%d-%H%M%S')}"
    llm = ScriptedLLM(env, args.seed) if args.offline else LLM()
    cfg = Config(steps=args.steps, tasks=args.tasks, tries=args.tries, seed=args.seed)
    Run(env, out, llm, cfg, knowledge_files=args.knowledge).go()
    print(f"run folder: {out}")


if __name__ == "__main__":
    main()

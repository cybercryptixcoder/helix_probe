"""The socket: the only thing the core knows about whatever it is probing.

An adapter is one file that subclasses `Environment`. The core never imports anything else from it.

Required:
    name          short id, used for run folders
    brief         what the experimenter is told about the box: what it may do, what comes back. Say as little about
                  the inner workings as you want it to discover.
    probe_format  the shape of one probe (the experiment's inputs) and of one observation (what comes back)
    probe(p)      run one experiment for real and return the observation (a JSON-able dict)

Optional, for any box:
    knowledge            given knowledge for the library
    validate(p)          an error string if a probe is malformed or out of range, else None
    compare(pred, obs)   how close a prediction is to an observation, 0..1 (default: `generic_compare`)
    random_probe(rng)    a random ordinary probe: used for the mixed experiments, and for the sealed exam and the
                         measurement-only held-out set when a run asks for them
    cost(p, obs)         what an experiment cost (default 1); runs can have a budget in these units

Optional, for boxes with state (a game, a machine: the box remembers, and experiments continue from where it is):
    stateful = True
    full_probe(p)        what the model is given to predict from: the probe plus where the box is now, e.g. the
                         current screen and every action since the last reset (so a model can keep its own memory of
                         anything the box remembers but doesn't show)
    view_state()         the box as it is now, in text, for the prompts
    restore(entries)     bring the box back to where a run stopped (e.g. replay its actions), for resuming

Optional, for boxes with goals:
    goal()               the current goal as a `Task`, or None if there is none (left); it may change as goals
                         are reached (levels)
    done()               True when there is nothing left to do (e.g. the game is won)
    plan_actions()       the single actions the planner may chain (a box with discrete actions)
    advance(fp, a, pred) the full probe for the state the model predicts after action `a` from full probe `fp`
                         (pred = the model's predicted observation); the planner walks the model with it
    state_key(fp)        a hashable key for a full probe's state, so the planner skips states already reached
    max_probe            the most actions one experiment may carry (a plan is run in pieces of this size)
    make_tasks(rng, n)   goals for a run to attempt after learning (stateless boxes)

Optional, for the prompts:
    view_probe(p), view_obs(o)   a compact text form of a probe / an observation (default: JSON)
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Task:
    description: str                      # told to the experimenter
    check: Callable[[dict], bool]         # observation -> achieved?


class Environment:
    name = "unnamed"
    brief = ""
    probe_format = ""
    knowledge = ""
    tolerance = 1e-6                      # numeric tolerance used by generic_compare
    stateful = False

    def probe(self, p: dict) -> dict:
        raise NotImplementedError

    def validate(self, p: dict) -> str | None:
        return None

    def compare(self, predicted: Any, observed: Any) -> float:
        return generic_compare(predicted, observed, self.tolerance)

    def random_probe(self, rng) -> dict | None:
        return None

    def cost(self, p: dict, obs: dict) -> float:
        return 1

    def full_probe(self, p: dict) -> dict:
        return p

    def view_state(self) -> str:
        return ""

    def restore(self, entries: list) -> None:
        return None

    def goal(self) -> Task | None:
        return None

    def done(self) -> bool:
        return False

    max_probe = 1

    def plan_actions(self) -> list:
        return []

    def advance(self, fp: dict, action, pred: dict) -> dict | None:
        return None

    def state_key(self, fp: dict):
        return json.dumps(fp, sort_keys=True)

    def make_tasks(self, rng, n: int) -> list[Task]:
        return []

    def view_probe(self, p: dict) -> str:
        return json.dumps(p, separators=(",", ":"))

    def view_obs(self, o: dict) -> str:
        return json.dumps(o, separators=(",", ":"))


def generic_compare(pred: Any, obs: Any, tol: float = 1e-6) -> float:
    """Fraction of the observation the prediction got right, recursively.

    dicts: mean over the observation's keys (a missing key scores 0); lists: mean over positions, a length mismatch
    counts the extra or missing positions as wrong; numbers: right if within `tol` (absolute or relative);
    everything else: equal or not.
    """
    if isinstance(obs, dict):
        if not isinstance(pred, dict) or not obs:
            return 1.0 if pred == obs else 0.0
        return sum(generic_compare(pred.get(k), v, tol) for k, v in obs.items()) / len(obs)
    if isinstance(obs, (list, tuple)):
        if not isinstance(pred, (list, tuple)):
            return 0.0
        n = max(len(obs), len(pred))
        if n == 0:
            return 1.0
        return sum(generic_compare(p, o, tol) for p, o in zip(pred, obs)) / n
    if isinstance(obs, bool) or isinstance(pred, bool):
        return 1.0 if pred == obs else 0.0
    if isinstance(obs, (int, float)) and isinstance(pred, (int, float)):
        if math.isnan(obs) or math.isnan(pred):
            return 0.0
        return 1.0 if abs(pred - obs) <= tol * max(1.0, abs(obs)) else 0.0
    return 1.0 if pred == obs else 0.0

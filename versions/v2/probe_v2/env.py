"""The socket: the only thing the core knows about whatever it is probing.

An adapter is one file that subclasses `Environment`. The core never imports anything else from it.

Required:
    name          short id, used for run folders
    brief         what the experimenter is told about the box: what it is allowed to do, what comes back.
                  Say as little about the inner workings as you want it to discover.
    probe_format  the shape of one probe (the experiment's inputs) and of one observation (what comes back)
    probe(p)      run one experiment for real and return the observation (a JSON-able dict)

Optional:
    knowledge     given knowledge for the library (rules, domain facts, tricks). Can also come from --knowledge files.
    validate(p)   return an error string if a probe is malformed or out of range, else None
    compare(pred, obs)   how close a prediction is to an observation, 0..1. Default: `generic_compare`.
    random_probe(rng)    a random valid probe. Used ONLY to build the held-out test set, which the experimenter
                         never sees: it is how we measure whether the model generalises.
    make_tasks(rng, n)   goals for solve mode, each a `Task`
"""
from __future__ import annotations

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

    def probe(self, p: dict) -> dict:
        raise NotImplementedError

    def validate(self, p: dict) -> str | None:
        return None

    def compare(self, predicted: Any, observed: Any) -> float:
        return generic_compare(predicted, observed, self.tolerance)

    def random_probe(self, rng) -> dict | None:
        return None

    def make_tasks(self, rng, n: int) -> list[Task]:
        return []


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

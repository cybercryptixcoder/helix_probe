"""FIND numeric functions (Schwettmann, Rott Shaham et al., NeurIPS 2023) as a box: f(x) on numbers.

    python -m probe.run envs/find_numeric.py --env-arg fid=f00012

The experimenter is told what FIND's own agents were told (FIND's numeric prompts), nothing more. Data from
bench/find/data (see bench/find/prepare.py). A probe evaluates f on up to 20 inputs, like FIND's
PYTHON(function.py v1 v2 ...) command.
"""
import importlib.util
import json
import math
from pathlib import Path

from probe.env import Environment

DATA = Path(__file__).resolve().parent.parent / "bench" / "find" / "data" / "numeric"

BRIEF = """A function f(x) that takes numerical inputs. Nobody has told you what it computes. In one experiment you \
call f on up to 20 values of x at once and read back the outputs. You can test values between -128 and 128. \
The output could be noisy. f(x) may combine multiple different operations. There may be an interval inside the \
domain where the function behaves differently; if so, your model should capture that interval and what happens in \
it."""
MLP_NOTE = " f(x) is implemented by a small neural network (an MLP) that approximates some function."


def load_function(fid, data=None):
    d = (Path(data) / "numeric" if data else DATA) / fid
    info = json.loads((d / "info.json").read_text())
    if info["kind"] == "mlp":
        import numpy as np
        w = json.loads((d / "weights.json").read_text())
        W1, b1, W2, b2 = (np.array(w[k]) for k in ("l0.weight", "l0.bias", "l2.weight", "l2.bias"))
        return info, lambda x: float((W2 @ np.maximum(W1[:, 0] * float(x) + b1, 0) + b2)[0])
    spec = importlib.util.spec_from_file_location(f"find_{fid}", d / "function_code.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return info, mod.function


def clean(v):
    try:
        v = float(v)
    except Exception:
        return None
    return None if math.isnan(v) or math.isinf(v) else round(v, 4)


class FindNumeric(Environment):
    probe_format = """probe:       {"x": [1.5, -20, 64]}      (1 to 20 numbers, each between -128 and 128)
observation: {"y": [f(1.5), f(-20), f(64)]}   (in the same order; null where f is undefined)"""

    def __init__(self, fid="f00000", data=None):
        self.info, self.f = load_function(fid, data)
        self.name = f"find_numeric_{fid}"
        self.brief = BRIEF + (MLP_NOTE if self.info["kind"] == "mlp" else "")

    def validate(self, p):
        xs = p.get("x")
        if not (isinstance(xs, list) and 1 <= len(xs) <= 20):
            return "x must be a list of 1 to 20 numbers"
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and -128 <= v <= 128 for v in xs):
            return "every x must be a number between -128 and 128"
        return None

    def probe(self, p):
        out = []
        for x in p["x"]:
            try:
                out.append(clean(self.f(float(x))))
            except Exception:
                out.append(None)
        return {"y": out}

    def compare(self, pred, obs):
        """Share of points within 5% of the value, plus 2% of the probe's typical size (so near-zero values and
        small wiggles don't count as misses)."""
        ys = obs.get("y", [])
        ps = pred.get("y") if isinstance(pred, dict) else None
        if not isinstance(ps, list) or len(ps) != len(ys):
            return 0.0
        finite = [abs(v) for v in ys if v is not None]
        rms = math.sqrt(sum(v * v for v in finite) / len(finite)) if finite else 0.0
        ok = 0
        for p, o in zip(ps, ys):
            if o is None:
                ok += p is None or not isinstance(p, (int, float)) or math.isnan(p) or math.isinf(p)
            elif isinstance(p, (int, float)) and not isinstance(p, bool) and math.isfinite(p):
                ok += abs(p - o) <= 0.05 * abs(o) + 0.02 * rms + 1e-6
        return ok / len(ys) if ys else 1.0

    def cost(self, p, obs):
        """FIND's unit of budget: inputs sent to the function."""
        return len(p.get("x") or [])

    def random_probe(self, rng):
        return {"x": [round(rng.uniform(-128, 128), 1) for _ in range(10)]}

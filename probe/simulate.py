"""Run the experimenter's model, predict(probe), on many probes in a separate process with a time limit.

The model is code the LLM wrote, so it never runs inside the core: a crash, an infinite loop or a stray import can
only cost that batch of predictions (all of them come back as None, which scores 0).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

RUNNER = r'''
import json, sys, traceback
src = open(sys.argv[1]).read()
probes = json.load(sys.stdin)
ns = {"__name__": "model"}
out = {"error": None, "predictions": []}
try:
    exec(compile(src, "model.py", "exec"), ns)
    predict = ns["predict"]
except Exception:
    out["error"] = traceback.format_exc(limit=2)[-1500:]
    predict = None
for p in probes:
    if predict is None:
        out["predictions"].append(None); continue
    try:
        r = predict(json.loads(json.dumps(p)))
        json.dumps(r)
        out["predictions"].append(r)
    except Exception as e:
        out["predictions"].append(None)
        if out["error"] is None:
            out["error"] = f"predict({json.dumps(p)[:200]}) raised {type(e).__name__}: {e}"[:1500]
print(json.dumps(out))
'''


def predict_many(code: str, probes: list[dict], timeout: float = 30.0) -> tuple[list, str | None]:
    """Returns (predictions aligned with probes, first error or None)."""
    if not probes:
        return [], None
    with tempfile.TemporaryDirectory() as d:
        model_path = os.path.join(d, "model.py")
        runner_path = os.path.join(d, "runner.py")
        with open(model_path, "w") as f:
            f.write(code)
        with open(runner_path, "w") as f:
            f.write(RUNNER)
        try:
            r = subprocess.run([sys.executable, "-I", runner_path, model_path], input=json.dumps(probes),
                               capture_output=True, text=True, timeout=timeout, cwd=d)
        except subprocess.TimeoutExpired:
            return [None] * len(probes), f"the model took longer than {timeout:.0f} s on {len(probes)} probes"
        try:
            out = json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:
            return [None] * len(probes), (r.stderr or "the model produced no output")[-1500:]
        return out["predictions"], out["error"]

"""FIND's official code-based scores, for any model: ours (predict(probe)) or a published FIND agent's code.py.

numeric  FIND's mse_indicator.py: evaluate on x = -127.5, -126.5, ..., 127.5 (skipping points where the true f is
         nan/inf); score 1 if sum((f - g)^2) / sum(f^2) < 0.1, else 0. Any error scores 0.
strings  FIND's string_indicator.py: for each of the function's 10 test vectors, take the correct (input, output)
         pair; score = share of pairs where the code's output equals the true output exactly.

Every candidate runs in a separate process with a time limit.
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import tempfile
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DATA = ROOT / "bench" / "find" / "data"
PUBLISHED = ROOT / "bench" / "find" / "published"
XS = [i + 0.5 for i in range(-128, 128)]

RUNNER = r'''
import json, sys, io, contextlib
spec = json.load(sys.stdin)
sys.path[:0] = [p for p in spec.get("path", []) if p not in sys.path]   # -I hides user site-packages (numpy)
ns = {"__name__": "candidate"}
out = {"outputs": None, "error": None}
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(open(sys.argv[1]).read(), "candidate.py", "exec"), ns)
        res = []
        if spec["mode"] == "predict":
            key_in, key_out, n = spec["key_in"], spec["key_out"], spec["chunk"]
            for i in range(0, len(spec["inputs"]), n):
                chunk = spec["inputs"][i:i + n]
                r = ns["predict"]({key_in: chunk})[key_out]
                if len(r) != len(chunk):
                    raise ValueError("predict returned the wrong number of outputs")
                res += list(r)
        else:
            f = ns[spec["fname"]]
            res = [f(x) for x in spec["inputs"]]
    out["outputs"] = [v if isinstance(v, (int, float, str)) or v is None else (float(v) if hasattr(v, "__float__") else str(v)) for v in res]
except Exception as e:
    out["error"] = f"{type(e).__name__}: {e}"[:500]
print(json.dumps(out, default=str))
'''


def run_candidate(code, spec, timeout=60):
    spec = {**spec, "path": [p for p in sys.path if p]}
    with tempfile.TemporaryDirectory() as d:
        Path(d, "c.py").write_text(code)
        Path(d, "r.py").write_text(RUNNER)
        try:
            r = subprocess.run([sys.executable, "-I", str(Path(d, "r.py")), str(Path(d, "c.py"))],
                               input=json.dumps(spec), capture_output=True, text=True, timeout=timeout, cwd=d)
            return json.loads(r.stdout.strip().splitlines()[-1])
        except Exception as e:
            return {"outputs": None, "error": f"{type(e).__name__}: {e}"[:300]}


@lru_cache(maxsize=None)
def numeric_truth(fid, data=None):
    from envs.find_numeric import load_function
    _, f = load_function(fid, data)
    xs, ys = [], []
    for x in XS:
        try:
            v = float(f(float(x)))
        except Exception:
            continue
        if not (math.isnan(v) or math.isinf(v)):
            xs.append(x)
            ys.append(v)
    return xs, ys


def strings_truth(fid, data=None):
    e = json.loads((Path(data or DATA) / "strings" / fid / "eval.json").read_text())
    pairs = []
    for vec, ci in zip(e["test_vec"], e["correct_inx"]):
        k = int(ci) - 1
        pairs.append((str(vec[0][k]), vec[1][k]))
    return pairs


def score_numeric(fid, code, published_fname=None, data=None):
    xs, ys = numeric_truth(fid, data)
    spec = ({"mode": "func", "fname": published_fname, "inputs": xs} if published_fname else
            {"mode": "predict", "key_in": "x", "key_out": "y", "chunk": 20, "inputs": xs})
    r = run_candidate(code, spec)
    try:
        g = [float(v) for v in r["outputs"]]
        if len(g) != len(ys) or any(math.isnan(v) or math.isinf(v) for v in g):
            raise ValueError
        nmse = sum((a - b) ** 2 for a, b in zip(ys, g)) / sum(a * a for a in ys)
    except Exception:
        return {"score": 0.0, "nmse": None, "error": r.get("error") or "unusable outputs"}
    return {"score": 1.0 if nmse < 0.1 else 0.0, "nmse": nmse, "error": None}


def score_strings(fid, code, published_fname=None, data=None):
    pairs = strings_truth(fid, data)
    ins = [p[0] for p in pairs]
    spec = ({"mode": "func", "fname": published_fname, "inputs": ins} if published_fname else
            {"mode": "predict", "key_in": "inputs", "key_out": "outputs", "chunk": 10, "inputs": ins})
    r = run_candidate(code, spec)
    if r["outputs"] is None or len(r["outputs"]) != len(pairs):
        return {"score": 0.0, "error": r.get("error") or "unusable outputs"}
    return {"score": sum(o == t for o, (_, t) in zip(r["outputs"], pairs)) / len(pairs), "error": None}


def score(category, fid, code, published_fname=None, data=None):
    return (score_numeric if category == "numeric" else score_strings)(fid, code, published_fname, data)


def published_fname(code):
    """FIND's own rule: the name of the last function defined in the file."""
    if "def " not in code:
        return ""
    return code.rsplit("def ", 1)[-1].split("(")[0].strip()


def score_published(category, fid, agent):
    p = PUBLISHED / agent / category / fid / "code.py"
    if not p.exists():
        return None
    code = p.read_text()
    name = published_fname(code)
    if not name:
        return {"score": 0.0, "error": "no function in code.py"}
    return score(category, fid, code, name)


if __name__ == "__main__":
    import argparse
    a = argparse.ArgumentParser(description="Score published FIND agents on the benchmark sample")
    a.add_argument("--out", default=str(ROOT / "bench" / "find" / "published_scores.json"))
    args = a.parse_args()
    sample = json.loads((DATA / "sample.json").read_text())
    agents = sorted(p.name for p in PUBLISHED.iterdir() if p.is_dir())
    res = {}
    for agent in agents:
        for cat, fids in sample.items():
            for fid in fids:
                s = score_published(cat, fid, agent)
                if s is not None:
                    res.setdefault(agent, {}).setdefault(cat, {})[fid] = s
    Path(args.out).write_text(json.dumps(res, indent=1))
    for agent, cats in res.items():
        print(agent, {c: f"{sum(v['score'] for v in d.values()) / len(d):.3f} (n={len(d)})" for c, d in cats.items()})

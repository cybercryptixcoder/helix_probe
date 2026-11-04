"""Official FIND score of every model version a run produced, as a curve over the experiments it had run.

    python bench/find/curve.py runs/x/find_strings_f00047 [more run folders]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from bench.find.score import score  # noqa: E402


def category_fid(run_dir: Path):
    if (run_dir / "bench.json").exists():
        b = json.loads((run_dir / "bench.json").read_text())
        return b["category"], b["fid"]
    name = json.loads((run_dir / "summary.json").read_text())["env"] if (run_dir / "summary.json").exists() else run_dir.name
    cat = "numeric" if "numeric" in name else "strings"
    return cat, name.rsplit("_", 1)[-1]


def versions(run_dir: Path):
    out = []
    for meta in sorted((run_dir / "model").glob("v*.json")):
        m = json.loads(meta.read_text())
        out.append((m["version"], m.get("made_at", 0), m.get("role", "?"), (run_dir / "model" / f"v{m['version']:03d}.py").read_text()))
    return out


def inputs_used(run_dir: Path):
    """Box inputs used: per experiment (cumulative), and by the exam."""
    nb = [json.loads(l) for l in (run_dir / "notebook.jsonl").read_text().splitlines() if l.strip()]
    size = lambda p: len(p.get("x") or p.get("inputs") or [])
    cum, t = [], 0
    for e in nb:
        t += size(e["probe"])
        cum.append(t)
    exam = json.loads((run_dir / "exam.json").read_text()) if (run_dir / "exam.json").exists() else []
    return cum, sum(size(x["probe"]) for x in exam), len(exam)


def curve(run_dir, cache=True):
    run_dir = Path(run_dir)
    path = run_dir / "official_curve.json"
    vs = versions(run_dir)
    if cache and path.exists():
        old = json.loads(path.read_text())
        if old.get("n_versions") == len(vs):
            return old
    cat, fid = category_fid(run_dir)
    data = json.loads((run_dir / "bench.json").read_text()).get("data") if (run_dir / "bench.json").exists() else None
    data = str(Path(__file__).resolve().parents[2] / data) if data else None
    cum, exam_inputs, exam_n = inputs_used(run_dir)
    pts = []
    for v, made_at, role, code in vs:
        s = score(cat, fid, code, data=data)
        pts.append({"version": v, "role": role, "experiments": made_at, "score": s["score"],
                    "nmse": s.get("nmse"), "inputs": (cum[made_at - 1] if made_at else 0) + exam_inputs})
    out = {"category": cat, "fid": fid, "experiments": len(cum), "exam_probes": exam_n, "n_versions": len(vs),
           "inputs_total": (cum[-1] if cum else 0) + exam_inputs,
           "final": pts[-1]["score"] if pts else 0.0, "points": pts}
    path.write_text(json.dumps(out, indent=1))
    return out


def at(c, experiments):
    """Official score of the model the run had after `experiments` experiments."""
    s = 0.0
    for p in c["points"]:
        if p["experiments"] <= experiments:
            s = p["score"]
    return s


if __name__ == "__main__":
    for d in sys.argv[1:]:
        c = curve(d, cache=False)
        print(d, "final", c["final"], [(p["experiments"], p["role"][0], p["score"]) for p in c["points"]])

"""One progress line for a FIND job: runs done, and the mean official score so far per arm and category."""
import json
import sys
import time
from pathlib import Path

job = Path(sys.argv[1])
cfg = json.loads((job / "job.json").read_text()) if (job / "job.json").exists() else {}
total = len(cfg.get("arms", [])) * sum(len(v[:cfg["limit"]] if cfg.get("limit") else v) for k, v in
                                        json.loads((Path(__file__).resolve().parents[2] / cfg["data"] / "sample.json").read_text()).items()
                                        if k in cfg.get("categories", [])) if cfg else 0
done, scores, calls = 0, {}, 0
for run in job.glob("*/*"):
    if (run / "calls.jsonl").exists():
        calls += sum(1 for _ in (run / "calls.jsonl").open())
    c = run / "official_curve.json"
    if (run / "summary.json").exists() and c.exists():
        done += 1
        d = json.loads(c.read_text())
        scores.setdefault(f"{run.parent.name} {d['category']}", []).append(d["final"])
parts = ", ".join(f"{k} {sum(v) / len(v):.2f} (n={len(v)})" for k, v in sorted(scores.items()))
print(time.strftime("== %H:%M progress: ") + f"{done}/{total} runs done, {calls} model calls; {parts}", flush=True)

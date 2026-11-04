"""Copy a FIND job's run folders into results/ for GitHub: every file, with each run's full model-call trace
(calls.jsonl) and every candidate model offered (offers.jsonl) gzipped deterministically (mtime 0), so a push only adds what changed. Then write the report.

    python bench/find/publish.py runs/find/find-v2 results/find/find-v2
"""
import gzip
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def main(src, dst):
    src, dst = Path(src), Path(dst)
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.glob("*.json"):
        shutil.copy2(f, dst / f.name)
    n = 0
    for run in sorted(p for p in src.glob("*/*") if p.is_dir()):
        out = dst / run.relative_to(src)
        out.mkdir(parents=True, exist_ok=True)
        for f in run.rglob("*"):
            if f.is_dir():
                continue
            rel = f.relative_to(run)
            (out / rel).parent.mkdir(parents=True, exist_ok=True)
            if f.name in ("calls.jsonl", "offers.jsonl"):
                target = out / (f.name + ".gz")
                data = f.read_bytes()
                with open(target, "wb") as fh, gzip.GzipFile(fileobj=fh, mode="wb", mtime=0, filename="") as gz:
                    gz.write(data)
            elif not f.name.endswith(".tmp"):
                shutil.copy2(f, out / rel)
        n += 1
    try:
        import contextlib, io, json
        arc = "budget_x" in json.loads((src / "job.json").read_text()) if (src / "job.json").exists() else False
        if arc:     # an ARC-AGI-3 job (bench/arc/run.py): same layout, its own report
            from bench.arc.run import report
        else:
            from bench.find.report import main as report
        with contextlib.redirect_stdout(io.StringIO()):
            report(str(src))
        for name in ("report.md", "report.json"):
            if (src / name).exists():
                shutil.copy2(src / name, dst / name)
    except Exception as e:
        print(f"   (the report failed: {e}; the run data are fine)")
    print(f"   published {n} runs to {dst}")


if __name__ == "__main__":
    main(*sys.argv[1:3])

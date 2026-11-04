"""Rebuild a job's run folders from what was pushed to GitHub, so a job can continue as if local storage was never lost.

publish.py copies every run file into results/ (calls.jsonl and offers.jsonl gzipped). This does the reverse:
results/<...>/<job> -> runs/<...>/<job>, unzipping the traces. Files already in the destination are kept unless
--force, so it is safe to run over a half-present folder. Then rerun the same job command with the same or a larger
--steps: finished runs are skipped, unfinished ones resume from their notebook, model and trial files.

    python bench/restore.py results/find/find-v3 runs/find/find-v3
"""
import argparse
import gzip
import shutil
from pathlib import Path


def restore(src, dst, force=False):
    src, dst = Path(src), Path(dst)
    if not src.exists():
        raise SystemExit(f"nothing to restore: {src} does not exist")
    copied = kept = 0
    for f in sorted(src.rglob("*")):
        if f.is_dir():
            continue
        rel = f.relative_to(src)
        gz = f.name.endswith(".jsonl.gz")
        target = dst / (rel.with_suffix("") if gz else rel)
        if target.exists() and not force:
            kept += 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if gz:
            with gzip.open(f, "rb") as fin, open(target, "wb") as fout:
                shutil.copyfileobj(fin, fout)
        else:
            shutil.copy2(f, target)
        copied += 1
    print(f"restored {copied} files into {dst} ({kept} already there, kept)")


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("src")
    a.add_argument("dst")
    a.add_argument("--force", action="store_true", help="overwrite files already in the destination")
    args = a.parse_args()
    restore(args.src, args.dst, args.force)

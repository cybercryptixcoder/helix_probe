"""Build the FIND sample used by Helix Probe's benchmark from FIND's public release.

FIND (Schwettmann, Rott Shaham et al., NeurIPS 2023, https://github.com/multimodal-interpretability/FIND, MIT).
Needs, once, on a machine with torch: FIND-dataset.zip (https://zenodo.org/record/8039658/files/FIND-dataset.zip)
and FIND's eval_data_strings.json (in the FIND repo: src/evaluate_interpretations/utils/). Writes
bench/find/data/, which is committed, so the benchmark itself needs only numpy and scipy.

    python bench/find/prepare.py --zip FIND-dataset.zip --strings-eval eval_data_strings.json

The numeric MLP functions (f00000-f00149) are converted from torch to plain weights (checked to match torch to
1e-4); every other function is copied as FIND wrote it.
"""
import argparse
import json
import random
import shutil
import tempfile
import zipfile
from pathlib import Path

OUT = Path(__file__).parent / "data"


def sample(meta, n, seed, key):
    """Stratified: round-robin over the atomic function names, so families are spread evenly."""
    rng = random.Random(seed)
    groups = {}
    for i, m in enumerate(meta):
        groups.setdefault(key(m), []).append(i)
    for g in groups.values():
        rng.shuffle(g)
    names = sorted(groups)
    rng.shuffle(names)
    picked = []
    while len(picked) < n and any(groups.values()):
        for nm in names:
            if groups[nm] and len(picked) < n:
                picked.append(groups[nm].pop())
    return sorted(picked)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--zip", required=True)
    a.add_argument("--strings-eval", required=True)
    a.add_argument("--numeric-mlp", type=int, default=10)
    a.add_argument("--numeric-code", type=int, default=30)
    a.add_argument("--strings", type=int, default=40)
    a.add_argument("--seed", type=int, default=2026)
    a.add_argument("--out", default=str(OUT), help="output folder (default: bench/find/data)")
    a.add_argument("--exclude", default=None, help="a sample.json whose functions must not be picked")
    args = a.parse_args()
    out_dir = Path(args.out)
    import numpy as np
    import torch
    global _load
    _load = torch.load

    tmp = Path(tempfile.mkdtemp())
    zipfile.ZipFile(args.zip).extractall(tmp)
    src = next(tmp.rglob("find_dataset"))
    if out_dir.exists():
        shutil.rmtree(out_dir)
    num_meta = json.loads((src / "numeric/data.json").read_text())
    str_meta = json.loads((src / "strings/data.json").read_text())
    str_eval = json.loads(Path(args.strings_eval).read_text())
    family = lambda m: m["name"].split("(")[0]
    ex = json.loads(Path(args.exclude).read_text()) if args.exclude else {"numeric": [], "strings": []}
    ex_n, ex_s = {int(f[1:]) for f in ex["numeric"]}, {int(f[1:]) for f in ex["strings"]}
    keep = lambda idx, meta, bad: ([i for i in idx if i not in bad], [meta[i] for i in idx if i not in bad])
    i1, m1 = keep(range(150), num_meta, ex_n)
    i2, m2 = keep(range(150, 1000), num_meta, ex_n)
    i3, m3 = keep(range(1000), str_meta, ex_s)
    mlp = [i1[j] for j in sample(m1, args.numeric_mlp, args.seed, family)]
    code = [i2[j] for j in sample(m2, args.numeric_code, args.seed, family)]
    strs = [i3[j] for j in sample(m3, args.strings, args.seed, family)]

    chosen = {"numeric": [], "strings": []}
    for i in mlp + code:
        fid = f"f{i:05d}"
        d = out_dir / "numeric" / fid
        d.mkdir(parents=True)
        info = {"fid": fid, "kind": "mlp" if i < 150 else "code", **num_meta[i]}
        if i < 150:
            sd = torch.load(src / "numeric" / fid / "mlp_approx_model.pt", map_location="cpu")
            w = {k.replace("layers.", "l"): v.numpy().tolist() for k, v in sd.items()}
            (d / "weights.json").write_text(json.dumps(w))
            # check against torch
            import importlib.util
            import functools
            torch.load = functools.partial(_load, map_location="cpu")   # FIND's own loader assumes a GPU
            spec = importlib.util.spec_from_file_location("gt", src / "numeric" / fid / "function_code.py")
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            W1, b1, W2, b2 = (np.array(w[k]) for k in ("l0.weight", "l0.bias", "l2.weight", "l2.bias"))
            for x in (-127.5, -3.0, 0.5, 42.0, 127.5):
                ours = float((W2 @ np.maximum(W1[:, 0] * x + b1, 0) + b2)[0])
                assert abs(ours - mod.function(x)) < 1e-4 * max(1, abs(ours)), (fid, x)
        else:
            shutil.copy(src / "numeric" / fid / "function_code.py", d / "function_code.py")
        (d / "info.json").write_text(json.dumps(info, indent=1))
        chosen["numeric"].append(fid)
    for i in strs:
        fid = f"f{i:05d}"
        d = out_dir / "strings" / fid
        d.mkdir(parents=True)
        shutil.copy(src / "strings" / fid / "function_code.py", d / "function_code.py")
        (d / "info.json").write_text(json.dumps({"fid": fid, **str_meta[i]}, indent=1))
        (d / "eval.json").write_text(json.dumps(str_eval[i]))
        chosen["strings"].append(fid)
    (out_dir / "sample.json").write_text(json.dumps(chosen, indent=1))
    (out_dir / "NOTICE.md").write_text(
        "Functions and evaluation data from FIND (Schwettmann, Rott Shaham, Materzynska, Chowdhury, Li, Andreas, "
        "Bau, Torralba; NeurIPS 2023 Datasets and Benchmarks), https://github.com/multimodal-interpretability/FIND, "
        "released under the MIT License. Numeric MLP weights converted from the released .pt files; everything else "
        "unchanged.\n")
    print({k: len(v) for k, v in chosen.items()})


if __name__ == "__main__":
    main()

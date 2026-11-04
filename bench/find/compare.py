"""The fair FIND comparison: Helix Probe against the same model run in FIND's own agent protocol (bench/find/aia.py),
function by function, at a matched budget, with paired statistics. FIND's published agents are listed alongside
on the same functions.

    python bench/find/compare.py --helix results/find/find-v3 --aia results/find/aia-none --out results/find/compare.md

For every function both have finished, and for every Helix Probe arm:
  final         Helix Probe's last model against the AIA's answer (Helix may have used a different budget)
  same inputs   Helix Probe's model at the point where it had sent the function no more inputs than the AIA did
                (FIND's own unit of budget; Helix's sealed-exam probes, if any, are counted)
  same exps     the same, counting experiments (calls to the function) instead of inputs
Paired statistics, standard library only: mean difference with a 95% bootstrap interval (10,000 resamples,
fixed seed), and wins / losses / ties with an exact two-sided sign test on the functions that differ.
"""
from __future__ import annotations

import argparse
import json
import random
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def rj(p):
    try:
        return json.loads(Path(p).read_text())
    except Exception:
        return None


def at_budget(points, key, limit):
    """Score of the last model whose budget (inputs or experiments) was within the limit; 0 if none was."""
    ok = [p for p in points if (p.get(key) or 0) <= limit]
    return ok[-1]["score"] if ok else 0.0


def sign_test(wins, losses):
    n = wins + losses
    if n == 0:
        return 1.0
    k = min(wins, losses)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def boot(diffs, n=10000, seed=0):
    if not diffs:
        return None, None
    rng = random.Random(seed)
    m = len(diffs)
    means = sorted(sum(rng.choice(diffs) for _ in range(m)) / m for _ in range(n))
    return means[int(.025 * n)], means[int(.975 * n) - 1]


def paired(ours, theirs):
    d = [a - b for a, b in zip(ours, theirs)]
    w, l = sum(x > 1e-9 for x in d), sum(x < -1e-9 for x in d)
    lo, hi = boot(d)
    return {"n": len(d), "ours": sum(ours) / len(d), "theirs": sum(theirs) / len(d), "diff": sum(d) / len(d),
            "ci": [lo, hi], "wins": w, "losses": l, "ties": len(d) - w - l, "p_sign": sign_test(w, l)}


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--helix", nargs="+", required=True, help="Helix Probe job folders (runs/ or results/)")
    a.add_argument("--aia", required=True, help="the AIA control's folder")
    a.add_argument("--out", help="write markdown here (and .json beside it)")
    args = a.parse_args()
    aia = {}
    for f in Path(args.aia).glob("*/result.json"):
        r = rj(f)
        if r:
            aia[(r["category"], r["fid"])] = r
    pub = rj(ROOT / "bench" / "find" / "published_scores.json") or {}
    report, lines = {}, ["# FIND: Helix Probe vs the same model in FIND's own protocol", "",
                         f"AIA control: `{args.aia}` ({len(aia)} functions). Scores: FIND's official scorer. "
                         "Paired over the functions both finished. CI: 95% bootstrap of the mean difference. "
                         "p: exact two-sided sign test on the functions that differ.", ""]
    for job in args.helix:
        for arm_dir in sorted(p for p in Path(job).iterdir() if p.is_dir()):
            for cat in ("numeric", "strings"):
                rows = []
                for f in sorted(arm_dir.glob(f"{cat}_*/official_curve.json")):
                    oc = rj(f)
                    key = (cat, f.parent.name.split("_", 1)[1])
                    if not oc or key not in aia or not (f.parent / "summary.json").exists():
                        continue
                    r = aia[key]
                    pts = oc.get("points", [])
                    rows.append({"fid": key[1], "aia": r["score"], "final": oc["final"],
                                 "same_inputs": at_budget(pts, "inputs", r.get("inputs") or 0),
                                 "same_exps": at_budget(pts, "experiments", r.get("experiments") or 0),
                                 "aia_inputs": r.get("inputs"), "helix_inputs": oc.get("inputs_total"),
                                 "aia_exps": r.get("experiments"), "helix_exps": oc.get("experiments")})
                if not rows:
                    continue
                th = [x["aia"] for x in rows]
                res = {k: paired([x[k] for x in rows], th) for k in ("final", "same_inputs", "same_exps")}
                fids = [x["fid"] for x in rows]
                res["published"] = {}
                for who in ("gpt-4", "gpt-3.5-turbo", "llama-2-70b"):
                    sc = (pub.get(who) or {}).get(cat) or {}
                    v = [sc[f]["score"] for f in fids if f in sc]
                    if len(v) == len(fids):
                        res["published"][who] = sum(v) / len(v)
                res["budget"] = {"aia_inputs": sum(x["aia_inputs"] or 0 for x in rows) / len(rows),
                                 "helix_inputs": sum(x["helix_inputs"] or 0 for x in rows) / len(rows),
                                 "aia_exps": sum(x["aia_exps"] or 0 for x in rows) / len(rows),
                                 "helix_exps": sum(x["helix_exps"] or 0 for x in rows) / len(rows)}
                res["rows"] = rows
                name = f"{Path(job).name}/{arm_dir.name}"
                report.setdefault(cat, {})[name] = res
    for cat, arms in report.items():
        lines += [f"## {cat}", "", "| Helix Probe arm | n | AIA (same model) | Helix final | Helix at the AIA's inputs | "
                  "diff [95% CI] | wins / losses / ties | p | Helix at the AIA's experiments | published GPT-4 |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
        for name, r in arms.items():
            s = r["same_inputs"]
            ci = s["ci"]
            lines.append(f"| {name} | {s['n']} | {s['theirs']:.2f} | {r['final']['ours']:.2f} | **{s['ours']:.2f}** | "
                         f"{s['diff']:+.2f} [{ci[0]:+.2f}, {ci[1]:+.2f}] | {s['wins']} / {s['losses']} / {s['ties']} | "
                         f"{s['p_sign']:.3g} | {r['same_exps']['ours']:.2f} | "
                         f"{r['published'].get('gpt-4', float('nan')):.2f} |")
        b = next(iter(arms.values()))["budget"]
        lines += ["", f"Budget per function (first arm): AIA {b['aia_exps']:.1f} experiments / {b['aia_inputs']:.0f} inputs; "
                      f"Helix Probe {b['helix_exps']:.1f} experiments / {b['helix_inputs']:.0f} inputs (exam included).", ""]
    text = "\n".join(lines) + "\n"
    print(text)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text)
        Path(args.out).with_suffix(".json").write_text(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

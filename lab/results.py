"""Collect every constructor run into readable results. Reads lab/constructions/<target>/<run id>/ and writes:

  lab/constructions/<target>/<run id>/README.md   one page per run: what the run was, the verdict, the mechanism in the
                                                  reader's words, where each variable lives, the test results, and
                                                  the commands that reproduce them
  lab/constructions/INDEX.md                      every run, grouped by network, best first
  docs/RESULTS_CONSTRUCTOR.md                     the results table: the best blinded run per network, and the controls

Run:  python3 lab/results.py        (safe to run at any time; it only reads runs and rewrites these files)
"""
import json, re, time
from pathlib import Path

LAB = Path(__file__).resolve().parent
CONS = LAB / "constructions"
DEV = {"bool_xor", "bool_parity3", "bool_compare2", "bool_majority3", "modadd_p113", "tracr_hist"}   # networks the constructor was developed on


def pct(v):
    return "n/a" if v is None else f"{100 * v:.1f}%"


def kind_of(cfg):
    if not cfg["weights"]:
        return "prior-only"
    if cfg["variant"] != "original":
        return cfg["variant"]
    return "told" if cfg["told"] else "blinded"


def rank(rep):
    if rep is None:
        return (-1, 0, 0)
    v = rep["verdict"]
    return (int(v.get("complete", False)), v.get("stages_verified", 0), rep["behaviour"]["match"])


def load(rdir):
    """A run's record and the judge's report on its delivered construction. Reports written by earlier versions of
    the judge lack some fields; they are filled in so that old runs still list."""
    rec = json.loads((rdir / "run.json").read_text())
    rep = json.loads((rdir / "report.json").read_text()) if (rdir / "report.json").exists() else None
    if rep is not None:
        v = rep["verdict"]
        v.setdefault("complete", False); v.setdefault("stages_verified", 0); v.setdefault("stages_total", len(rep.get("stages", {})) or 1)
        rep.setdefault("stages", {})
    return rec, rep


def description(src):
    m = re.search(r'DESCRIPTION\s*=\s*(\(?\s*(?:"""[\s\S]*?"""|(?:"(?:[^"\\]|\\.)*"\s*)+)\s*\)?)', src)
    if not m:
        return ""
    try:
        return " ".join(str(eval(m.group(1))).split())      # a string literal from the construction file
    except Exception:  # noqa: BLE001
        return ""


def run_readme(target, rdir, rec, rep, meta):
    cfg = rec["config"]
    L = [f"# Construction run `{rec['id']}` on `{target}`", "",
         f"*Written by `lab/results.py` from the files in this folder. Network: {meta.get('name', target)} "
         f"({meta.get('params', 0):,} weights). Known answer (never shown to a blinded reader): {meta['answer']['short']}.*", "",
         "## The run", "",
         f"- Reader: {cfg['model']}, reasoning effort {cfg['effort']}; step budget {cfg['max_steps']}; "
         f"used {len(rec['steps'])} steps, {len(rec['submissions'])} submissions, {rec.get('seconds', 0):.0f} s, ${rec.get('cost', 0):.3f}.",
         f"- Weights: {cfg['variant']}. Reader was {'told the task' if cfg['told'] else 'blinded (not told what the network does)'}"
         f"{'' if cfg['weights'] else ', had NO weights and could not run the network (prior-only control)'}"
         f"{', and had a single submission with no report back' if cfg.get('one_shot') else ''}.",
         f"- Title: {cfg.get('title') or '(none)'}. Status: {rec['status']}.", ""]
    if rep is None:
        L += ["## Result", "", "No submission could be judged.", ""]
    else:
        v, b = rep["verdict"], rep["behaviour"]
        L += ["## Result", "",
              ("**VERIFIED AND COMPLETE**: every stage of the network has a verified site." if v["complete"] else
               f"**{v['stages_verified']} of {v['stages_total']} stages verified**" + (" (every site the delivered construction names passes)." if v["verified"] else ".")),
              "", f"Run in place of the network, the construction makes the same decision on {pct(b['match'])} of {rep['n_test']} held-out inputs "
              f"(a constant output: {pct(b['baseline_constant_match'])}). Construction length: {rep['source_chars']:,} characters.", ""]
        src = (rdir / "construction.py").read_text()
        d = description(src)
        if d:
            L += ["## The mechanism, in the reader's words", "", d, ""]
        if rec.get("final_message"):
            L += ["## The reader's final summary", "", rec["final_message"].strip(), ""]
        L += ["## Stages", "", "| Stage | Status | Sites |", "|---|---|---|"]
        for name, st in rep["stages"].items():
            status = "verified" if st["verified"] else ("named, failing" if st["named"] else "not explained")
            L.append(f"| {name} | {status} | {', '.join(st['verified'] or st['named'] or st['sites'])} |")
        L += ["", "## Where each variable lives", "", "| Variable | Dimensions | Sites |", "|---|---|---|"]
        for name, var in rep["variables"].items():
            L.append(f"| `{name}` | {var['dim']} | {', '.join(var['sites']) or '(not aligned)'} |")
        L += ["", "## Site tests", "",
              "Substitute: decisions kept when the site is replaced by the construction's prediction. Remove: decisions kept when the "
              "named subspace is removed. Mean-ablate: decisions kept when the whole site is replaced by its mean.", "",
              "| Site | Named dims / PCs that suffice | Variance explained | Substitute | Remove | Mean-ablate | Pass |", "|---|---|---|---|---|---|---|"]
        for s, r in rep["sites"].items():
            L.append(f"| `{s}` | {r['named_rank']} / {r.get('pca_sufficient_rank', 'n/a')} | {r['explained']:.2f} | {pct(r['substitute_match'])} | "
                     f"{pct(r['remove_named_match'])} | {pct(r['mean_ablate_match'])} | {'yes' if r.get('pass') else 'no'} |")
        L += ["", "## Intervention tests", "",
              "Share of cases where the predictor named the network's new decision, among cases where the decision changed "
              "(\"no change\" scores 0 on these by definition).", "",
              "| Test | Variable | Site | Construction | Source output | Attribution patching | Pass |", "|---|---|---|---|---|---|---|"]
        for t in rep["interventions"]:
            L.append(f"| {t['mode']} | `{t['variable']}` | `{t['site']}` | {pct(t['agreement_when_changed'] if t['agreement_when_changed'] is not None else t['agreement'])} | "
                     f"{pct(t['baseline_source_output'])} | {pct(t.get('attribution_patching_when_changed', t.get('attribution_patching')))} | {'yes' if t.get('pass') else 'no'} |")
        if v["fails"]:
            L += ["", "## What fails", ""] + [f"- {f}" for f in v["fails"]]
        if rec.get("pruned_sites"):
            L += ["", f"Sites the reader's best submission named that failed, and that the delivered construction therefore does not claim: "
                      f"{', '.join(rec['pruned_sites'])}."]
    rel = f"lab/constructions/{target}/{rec['id']}"
    variant = "" if cfg["variant"] == "original" else f" --variant {cfg['variant']}"
    L += ["", "## Files", "",
          "- `construction.py`: the delivered construction (runnable: `model(x, iv)` and `ALIGN`).",
          "- `report.txt`, `report.json`: the judge's report on it.",
          "- `submission_NN.py`, `submission_NN.json`: every construction the reader submitted, with its report.",
          "- `run.json`: the whole run: prompt, every step (reasoning, code, outputs), usage.",
          "- `predict.json` (if present): the held-out intervention benchmark.", "",
          "## Reproduce", "", "```bash",
          f"python3 lab/judge.py {target} {rel}/construction.py{variant}        # re-run every test on the delivered construction",
          f"python3 lab/predict.py {target} {rel}/construction.py              # held-out interventions against the baselines",
          f"python3 lab/constructor.py {target}{variant}{' --told' if cfg['told'] else ''}{' --no-weights' if not cfg['weights'] else ''}"
          f"{' --one-shot' if cfg.get('one_shot') else ''} --steps {cfg['max_steps']}   # a fresh run with the same settings (needs lab/.env)",
          "```", ""]
    (rdir / "README.md").write_text("\n".join(L))


def main():
    rows = []
    for tdir in sorted(p for p in CONS.iterdir() if p.is_dir() and not p.name.startswith("_")):
        meta = json.loads((LAB / "models" / tdir.name / "meta.json").read_text())
        for rdir in sorted(p for p in tdir.iterdir() if (p / "run.json").exists()):
            rec, rep = load(rdir)
            if rec["status"] != "running":
                run_readme(tdir.name, rdir, rec, rep, meta)
            rows.append({"target": tdir.name, "id": rec["id"], "kind": kind_of(rec["config"]), "rec": rec, "rep": rep, "meta": meta})

    def line(r):
        rec, rep = r["rec"], r["rep"]
        v = rep["verdict"] if rep else None
        res = "no construction" if v is None else ("**complete**" if v["complete"] else f"{v['stages_verified']} of {v['stages_total']} stages")
        beh = pct(rep["behaviour"]["match"]) if rep else "n/a"
        return (f"| [`{r['id']}`]({r['target']}/{r['id']}/README.md) | {r['kind']} | {rec['config'].get('title', '')} | {rec['status']} | {res} | {beh} | "
                f"{len(rec['steps'])} | {len(rec['submissions'])} | ${rec.get('cost', 0):.2f} |")

    idx = ["# Constructor runs", "", f"*Written by `lab/results.py` on {time.strftime('%Y-%m-%d %H:%M')}. Every run of `lab/constructor.py`, grouped by network, best first. "
           "Each run id links to that run's page.*", ""]
    for t in sorted({r["target"] for r in rows}):
        mine = sorted([r for r in rows if r["target"] == t], key=lambda r: (r["kind"] != "blinded", [-x for x in rank(r["rep"])]))
        idx += [f"## `{t}`: {mine[0]['meta']['answer']['short']}", "",
                "| Run | Reader | Title | Status | Result | Behaviour match | Steps | Submissions | Cost |", "|---|---|---|---|---|---|---|---|---|"]
        idx += [line(r) for r in mine] + [""]
    (CONS / "INDEX.md").write_text("\n".join(idx))

    # the results table: best finished blinded run on trained weights per network, then controls
    out = ["# Constructor results", "",
           f"*Written by `lab/results.py` on {time.strftime('%Y-%m-%d %H:%M')} from the run folders in `lab/constructions/`. Do not edit by hand; "
           "rerun the script. The reader is DeepSeek V4.1 Flash. \"Blinded\" means the reader was given the architecture, the weights and the "
           "input set, and was not told what the network does. Development networks are the ones the constructor's prompt and the judge were "
           "worked out on; held-out networks were run only after both were frozen.*", "",
           "## Best blinded run per network (trained weights)", "",
           "| Network | What it computes (hidden from the reader) | Used in development? | Stages verified | Behaviour match | Steps | Run |",
           "|---|---|---|---|---|---|---|"]
    for t in sorted({r["target"] for r in rows}):
        cands = [r for r in rows if r["target"] == t and r["kind"] == "blinded" and r["rec"]["status"] != "running" and "frontend" not in r["rec"]["config"].get("title", "")]
        if not cands:
            continue
        best = max(cands, key=lambda r: rank(r["rep"]))
        rep = best["rep"]
        v = rep["verdict"] if rep else None
        res = "none" if v is None else (f"**all {v['stages_total']} (complete)**" if v["complete"] else f"{v['stages_verified']} of {v['stages_total']}")
        n_runs = len(cands)
        out.append(f"| `{t}` | {best['meta']['answer']['short']} | {'yes' if t in DEV else '**no (held out)**'} | {res} | {pct(rep['behaviour']['match']) if rep else 'n/a'} | "
                   f"{len(best['rec']['steps'])} | [`{best['id']}`](../lab/constructions/{t}/{best['id']}/README.md) (best of {n_runs}) |")
    out += ["", "## Controls", "",
            "Shuffled and untrained weights should give no verified construction; permuted weights (the same function, units reordered) should "
            "give the same one; the prior-only reader (task named, no weights, one submission) shows what memory alone gives.", "",
            "| Network | Control | Stages verified | Behaviour match | Steps | Run |", "|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["target"], r["kind"], r["id"])):
        if r["kind"] in ("blinded", "told") or r["rec"]["status"] == "running":
            continue
        rep = r["rep"]
        v = rep["verdict"] if rep else None
        res = "no construction" if v is None else f"{v['stages_verified']} of {v['stages_total']}"
        out.append(f"| `{r['target']}` | {r['kind']} | {res} | {pct(rep['behaviour']['match']) if rep else 'n/a'} | {len(r['rec']['steps'])} | "
                   f"[`{r['id']}`](../lab/constructions/{r['target']}/{r['id']}/README.md) {r['rec']['config'].get('title', '')} |")
    out += ["", "All runs, including failed and superseded ones: [`lab/constructions/INDEX.md`](../lab/constructions/INDEX.md). "
            "What each experiment was for and what was concluded: [`EXPERIMENT_LOG.md`](EXPERIMENT_LOG.md).", ""]
    (LAB.parent / "docs" / "RESULTS_CONSTRUCTOR.md").write_text("\n".join(out))
    print(f"{len(rows)} runs; wrote lab/constructions/INDEX.md, docs/RESULTS_CONSTRUCTOR.md and a README.md in each finished run folder")


if __name__ == "__main__":
    main()

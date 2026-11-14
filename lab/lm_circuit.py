"""From a verified construction of a language-model behaviour to a circuit: which components WRITE each variable.

The residual stream at depth L and position p is a sum:  embedding + sum over layers l < L of (heads of layer l + MLP l)
at that position. A variable the construction places at resid{L}@p is read from the residual stream by a linear probe
(the judge's read map). The probe is linear, so the read-out splits exactly into one part per component. For each
variable and each site this gives every component's SHARE of the variable (the covariance of the component's part
with the variable, over the variable's variance; the shares of all components add up to the probe's R2). For the
heads with a large share, the mean attention pattern says which positions they take it from. Each top component is
then checked causally: with its output at p replaced by its mean, how much of the variable is left in the residual
stream, and how many of the network's answers survive.

Run:  python3 lab/lm_circuit.py <target> <run id | construction.py>      (writes circuit.json / circuit.txt in the run folder)
"""
import json, sys
from pathlib import Path

import numpy as np

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB))
import judge as J  # noqa: E402
import lm          # noqa: E402

TOP = 6            # components listed per variable and site
MAX_N = 400


def circuit(tid, source, only_units=None, seed=0):
    task = lm.get_task(tid)
    model, align = J.load_construction(source)
    rng = np.random.default_rng(seed)
    idx = np.sort(rng.choice(task.N, min(task.N, MAX_N), replace=False))
    X = task.X[idx]
    _, vals = J.run_model(model, X)
    out = task.run(idx)
    dec = out.argmax(1)
    H, T = task.cfg["n_heads"], task.T
    pos_names = {}
    for r, p in task.roles.items():
        if len(set(p.tolist())) == 1:
            pos_names.setdefault(int(p[0]), r)
    res = {"target": tid, "n_prompts": len(idx), "variables": []}
    sites = sorted({s for where in align.values() for s in where if lm.parse_site(s)[0] == "resid"}, key=lambda s: (lm.parse_site(s)[1], s))
    for s in sites:
        _, L, _, pos = lm.parse_site(s)
        if only_units is not None and f"cut{L}" not in only_units:
            continue
        names = [v for v in vals if s in align.get(v, [])]
        if not names or L == 0:
            continue
        A = task.resid(L, idx, pos)
        c = A.mean(0)
        if (A - c).std() < 1e-6:
            continue
        # every component's output at this position, layers < L
        comp_sites = [f"head{l}.{h}@{pos}" for l in range(L) for h in range(H)] + [f"mlp{l}@{pos}" for l in range(L)]
        acts = task.acts(idx, comp_sites)
        parts = {"embedding": task.resid(0, idx, pos)}
        parts.update({cs.split("@")[0]: acts[cs] for cs in comp_sites})
        _, sv, Vt = np.linalg.svd(A - c, full_matrices=False)
        rr = max(1, min(int((sv > 1e-6 * sv[0]).sum()), max(8, len(idx) // 4)))
        Z = (A - c) @ Vt[:rr].T
        for v in names:
            V = vals[v] - vals[v].mean(0)
            if V.var(0).sum() < 1e-12:
                continue
            Dz, *_ = np.linalg.lstsq(Z, V, rcond=1e-6)
            D = Vt[:rr].T @ Dz                                    # [d, k]: the probe
            tot = float((V ** 2).sum())
            r2 = float(1 - (((A - c) @ D - V) ** 2).sum() / tot)
            shares = {name: float((((a - a.mean(0)) @ D) * V).sum() / tot) for name, a in parts.items()}
            top = sorted(shares.items(), key=lambda kv: -abs(kv[1]))[:TOP]
            rows = []
            for name, sh in top:
                row = {"component": name, "share": round(sh, 4)}
                if name.startswith("head"):
                    l, h = map(int, name[4:].split("."))
                    pat = task.acts(idx, [f"pattern{l}.{h}@{pos}"])[f"pattern{l}.{h}@{pos}"].mean(0)
                    order = np.argsort(-pat)[:3]
                    row["attends"] = [[pos_names.get(int(j), str(int(j))), round(float(pat[j]), 3)] for j in order if pat[j] > 0.05]
                if name != "embedding":
                    site = f"{name}@{pos}"
                    a = parts[name]
                    o, got = task.run(idx, hook={site: np.broadcast_to(a.mean(0), a.shape)}, sites=[s])
                    left = float(1 - (((got[s] - c) @ D - V) ** 2).sum() / tot)
                    row["variable_r2_without"] = round(left, 4)
                    row["answers_kept_without"] = round(float((o.argmax(1) == dec).mean()), 4)
                rows.append(row)
            res["variables"].append({"variable": v, "site": s, "dim": int(V.shape[1]), "probe_r2": round(r2, 4), "components": rows,
                                     "by_layer": {f"layer {l}": round(sum(sh for n, sh in shares.items() if n != "embedding" and int(n.replace("head", "").replace("mlp", "").split(".")[0]) == l), 4) for l in range(L)},
                                     "embedding_share": round(shares["embedding"], 4)})
    return res


def render(res):
    L = [f"CIRCUIT  which components write each variable ({res['n_prompts']} prompts). share = the component's part of the variable's "
         "read-out (all components add up to the probe's R2). without = with that component's output at the position replaced by its "
         "mean: the variable's R2 left in the residual stream / the share of the network's answers kept."]
    for e in res["variables"]:
        L.append(f"{e['variable']} @ {e['site']}  ({e['dim']} dims; probe R2 {e['probe_r2']:.2f}; embedding share {e['embedding_share']:+.2f})")
        L.append("    by layer: " + "  ".join(f"{k.split()[1]}:{v:+.2f}" for k, v in e["by_layer"].items()))
        for r in e["components"]:
            if r["component"] == "embedding":
                continue
            att = ("  attends " + ", ".join(f"{a} {w:.2f}" for a, w in r["attends"])) if r.get("attends") else ""
            L.append(f"    {r['component']:10s} share {r['share']:+.2f} | without: variable R2 {r['variable_r2_without']:.2f}, answers kept {r['answers_kept_without']:.1%}{att}")
    return "\n".join(L)


def for_run(tid, rid):
    rdir = LAB / "constructions" / tid / rid
    src = (rdir / "construction.py").read_text() if (rdir / "construction.py").exists() else None
    rep = json.loads((rdir / "report.json").read_text()) if (rdir / "report.json").exists() else None
    if src is None:                       # a run still going or interrupted: its best submission
        rec = json.loads((rdir / "run.json").read_text())
        n = rec.get("best")
        if not n:
            return {"error": "this run has no construction yet"}
        src = (rdir / f"submission_{n:02d}.py").read_text()
        rep = json.loads((rdir / f"submission_{n:02d}.json").read_text())
    verified = [u for u, r in rep["sites"].items() if r.get("pass")] if rep else None
    res = circuit(tid, src, only_units=verified)
    res["text"] = render(res)
    (rdir / "circuit.json").write_text(json.dumps(res, indent=1))
    (rdir / "circuit.txt").write_text(res["text"] + "\n")
    return res


if __name__ == "__main__":
    tid, what = sys.argv[1], sys.argv[2]
    if Path(what).exists():
        print(render(circuit(tid, Path(what).read_text())))
    else:
        print(for_run(tid, what).get("text"))

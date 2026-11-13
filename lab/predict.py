"""Does a construction predict interventions it was never tested on, better than methods that understand nothing?

The benchmark. Interventions are drawn without looking at any construction. Each acts on a subspace Q of one site's
activation, in one of two ways:
  remove   the subspace is removed (measured from the site's mean):       act' = act - (act - mean) Q Q^T
  patch    the subspace is copied in from another input's run (source):   act' = act + (act_source - act) Q Q^T
Four kinds of subspace:
  random     a random subspace of 1 to 32 dimensions
  units      a random subset of the site's own units (neurons or residual coordinates)
  top_pca    some of the site's largest principal components
  pca_mix    a random subspace inside the site's 24 largest principal components
At a residual-stream site such an activation edit equals a weight edit (project the matrices that write to the
stream), so these are also weight edits. The truth for each (intervention, input) is the network's decision after
the intervention. Half of the interventions and half of the inputs are held out for scoring.

The predictors:
  construction   the construction file with its alignment (fitted on clean activations of the fit inputs only). It
                 translates the removed subspace into a change of its variables at that site and runs model(). It
                 never runs the network. At a site the construction does not align to, it predicts "no change".
  no_change      the behaviour-only surrogate: it knows the input-output function and nothing inside, so it predicts
                 that the decision stays. (source_output: for patches, predicts the source input's decision.)
  statistics     a regressor on statistics of the intervention (site, size, share of activation variance removed,
                 share of the next weight matrix's norm touched), trained on the training interventions to predict
                 the share of decisions kept; an input is predicted "changed" when that share is below one half.
  attribution    attribution patching: the first-order estimate  out + d(out)/d(act) . (act' - act), computed on the
                 real network (it needs the network at prediction time; the construction does not).
  another construction (for example the prior-only one) can be passed with --also name=path.

Scores (held-out interventions x held-out inputs):
  decision accuracy       the predicted decision equals the network's decision after the intervention
  ... when changed        the same, over the cases where the network's decision changed
  ... when unchanged      the same, over the cases where it did not
  kept: correlation/error Spearman correlation and mean absolute error between predicted and true share of decisions
                          kept, across interventions

Run:  python3 lab/predict.py <target id> <construction.py> [--also prior=path.py] [--json out.json] [--n 40]
"""
import argparse, json, sys
from pathlib import Path

import numpy as np

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB))
import nets   # noqa: E402
import judge  # noqa: E402


def draw_interventions(acts, sites, fit, rng, n_per_site):
    out = []
    for s in sites:
        A = acts[s]
        d = A.shape[1]
        c = A[fit].mean(0)
        _, sv, Vt = np.linalg.svd(A[fit] - c, full_matrices=False)
        live = int((sv > 1e-9 * max(sv[0], 1e-12)).sum())
        for i in range(n_per_site):
            kind = ["random", "units", "top_pca", "pca_mix"][i % 4]
            if kind == "random":
                r = int(rng.choice([1, 2, 4, 8, 16, 32]))
                Q, _ = np.linalg.qr(rng.normal(size=(d, min(r, d - 1))))
            elif kind == "units":
                k = max(1, int(d * rng.choice([0.02, 0.05, 0.1, 0.2, 0.4])))
                Q = np.eye(d)[:, rng.choice(d, k, replace=False)]
            elif kind == "top_pca":
                top = min(live, 24)
                k = int(rng.integers(1, max(2, top // 2 + 1)))
                Q = Vt[rng.choice(top, min(k, top), replace=False)].T
            else:
                top = min(live, 24)
                k = int(rng.integers(1, max(2, top // 2 + 1)))
                B, _ = np.linalg.qr(rng.normal(size=(top, min(k, top))))
                Q = Vt[:top].T @ B
            out.append({"site": s, "kind": kind, "dims": int(Q.shape[1]), "Q": Q, "mode": "remove" if (i // 4) % 2 == 0 else "patch"})
    return out


class Construction:
    """A construction with its alignment fitted on clean activations of the fit inputs."""
    def __init__(self, source, kind, W, X, acts, fit):
        self.model, align = judge.load_construction(source)
        sites = {name for name, *_ in nets.site_table(kind, W)}
        self.out, self.vals = judge.run_model(self.model, X)
        self.X = X
        self.sites = {}
        for s in sorted({s for w in align.values() for s in w if s in sites and acts[s].std(0).max() > 1e-9}):
            names = [v for v in self.vals if s in align.get(v, [])]
            cols, k0 = {}, 0
            for v in names:
                cols[v] = np.arange(k0, k0 + self.vals[v].shape[1]); k0 += self.vals[v].shape[1]
            V = np.concatenate([self.vals[v] for v in names], 1)
            c, vmu, M, D = judge.fit_alignment(V, acts[s], fit)
            # Mp reads variable coordinates off the named subspace: the construction's claim is that the rest of the
            # activation does not matter, so the part of an edit outside the named subspace is predicted to do nothing
            self.sites[s] = {"names": names, "cols": cols, "V": V, "vmu": vmu, "M": M, "Mp": np.linalg.pinv(M, rcond=1e-8)}

    def predict(self, iv, idx, src):
        """The predicted network output on inputs idx after intervention iv (src: the source inputs, for a patch).
        Uses the construction only."""
        a = self.sites.get(iv["site"])
        if a is None:
            return self.out[idx]
        V = a["V"][idx]
        delta = (a["V"][src] - V) if iv["mode"] == "patch" else -(V - a["vmu"])
        d_act = ((delta @ a["M"]) @ iv["Q"]) @ iv["Q"].T                # the construction's own account of the activation change
        V2 = V + d_act @ a["Mp"]                                        # ... read back as a change of its variables
        out, _ = judge.run_model(self.model, self.X[idx], {v: V2[:, a["cols"][v]] for v in a["names"]})
        return out


def run(target, source, also=(), n_per_site=40, seed=0, max_inputs=1500, variant="original"):
    meta, W, X = judge.load_target(target, variant)
    kind = meta["forward"]
    judge.GROUPS = meta.get("out_groups")
    rng = np.random.default_rng(seed)
    acts = {}
    out = nets.forward(kind, W, X, acts=acts)
    N = len(X)
    perm = rng.permutation(N)
    fit, test = (perm[: N // 2], perm[N // 2:]) if N >= 200 else (np.arange(N), np.arange(N))
    test = test[:max_inputs]
    src = rng.permutation(test)                                         # the source input paired with each test input (for patches)
    sites = [name for name, *_ in nets.site_table(kind, W) if name != "out" and acts[name].std(0).max() > 1e-9]
    ivs = draw_interventions(acts, sites, fit, rng, n_per_site)
    order = rng.permutation(len(ivs))
    train_iv, test_iv = set(order[: len(ivs) // 2].tolist()), set(order[len(ivs) // 2:].tolist())

    cons = {"construction": Construction(source, kind, W, X, acts, fit)}
    for name, other_source in also:
        cons[name] = Construction(other_source, kind, W, X, acts, fit)

    # the truth, attribution patching, and the statistics of every intervention
    nxt = next_weights(kind, W)
    rows = []
    for k, iv in enumerate(ivs):
        s, Q = iv["site"], iv["Q"]
        A = acts[s]
        c = A[fit].mean(0)
        d_act = (((A[src] - A[test]) if iv["mode"] == "patch" else -(A[test] - c)) @ Q) @ Q.T
        truth = nets.forward(kind, W, X[test], hook={s: A[test] + d_act})
        eps = 1e-3
        lin = out[test] + (nets.forward(kind, W, X[test], hook={s: A[test] + eps * d_act}) - out[test]) / eps
        var = float(((A[fit] - c) @ Q).__pow__(2).sum() / max(((A[fit] - c) ** 2).sum(), 1e-12))
        wn = nxt.get(s)
        wshare = float((np.linalg.norm(Q.T @ wn) ** 2) / max(np.linalg.norm(wn) ** 2, 1e-12)) if wn is not None else 0.0
        rows.append({"k": k, "site": s, "kind": iv["kind"], "mode": iv["mode"], "dims": iv["dims"], "width": A.shape[1], "var_removed": var, "next_weight_share": wshare,
                     "truth": truth, "attribution": lin, "kept": judge.match(truth, out[test])})
    # statistics + regressor (trained on the training interventions)
    from sklearn.ensemble import GradientBoostingRegressor
    feat = lambda r: [sites.index(r["site"]), float(r["mode"] == "patch"), r["dims"], r["dims"] / r["width"], r["var_removed"], r["next_weight_share"]]   # noqa: E731
    tr = [r for r in rows if r["k"] in train_iv]
    reg = GradientBoostingRegressor(n_estimators=200, max_depth=3, random_state=0).fit([feat(r) for r in tr], [r["kept"] for r in tr])
    for r in rows:
        r["stat_kept"] = float(np.clip(reg.predict([feat(r)])[0], 0, 1))

    names = list(cons) + ["no_change", "source_output", "statistics", "attribution"]
    score = {n: {"right": [], "changed": [], "kept_pred": [], "kept_true": [], "site": [], "mode": []} for n in names}
    for r in rows:
        if r["k"] not in test_iv:
            continue
        iv, truth = ivs[r["k"]], r["truth"]
        changed = ~judge.same(truth, out[test])
        preds = {n: c.predict(iv, test, src) for n, c in cons.items()}
        preds["no_change"] = out[test]
        preds["source_output"] = out[src] if iv["mode"] == "patch" else out[test]
        preds["attribution"] = r["attribution"]
        for n in names:
            if n == "statistics":
                right = (~changed) if r["stat_kept"] >= 0.5 else np.zeros(len(test), bool)      # "changed" names no new decision
                kept_pred = r["stat_kept"]
            else:
                right = judge.same(preds[n], truth)
                kept_pred = judge.match(preds[n], out[test])
            sc = score[n]
            sc["right"].append(right); sc["changed"].append(changed); sc["kept_pred"].append(kept_pred)
            sc["kept_true"].append(r["kept"]); sc["site"].append(r["site"]); sc["mode"].append(r["mode"])

    from scipy.stats import spearmanr
    aligned = set(cons["construction"].sites)
    res = {"target": target, "n_interventions_scored": len(test_iv), "n_inputs": len(test), "sites": sites,
           "sites_aligned_by_construction": sorted(aligned), "predictors": {}}
    for n in names:
        sc = score[n]
        def summarise(mask):
            if not mask.any():
                return None
            right = np.concatenate([x for x, m in zip(sc["right"], mask) if m])
            ch = np.concatenate([x for x, m in zip(sc["changed"], mask) if m])
            kp, kt = np.array(sc["kept_pred"])[mask], np.array(sc["kept_true"])[mask]
            rho = spearmanr(kp, kt).statistic if len(kp) > 2 and kp.std() > 0 and kt.std() > 0 else None
            return {"decision_accuracy": float(right.mean()),
                    "accuracy_when_changed": float(right[ch].mean()) if ch.any() else None,
                    "accuracy_when_unchanged": float(right[~ch].mean()) if (~ch).any() else None,
                    "share_changed": float(ch.mean()),
                    "kept_spearman": None if rho is None or np.isnan(rho) else float(rho),
                    "kept_mae": float(np.abs(kp - kt).mean()), "n_interventions": int(mask.sum())}
        site_arr, mode_arr = np.array(sc["site"]), np.array(sc["mode"])
        al = np.isin(site_arr, sorted(aligned))
        res["predictors"][n] = {"all_sites": summarise(np.ones(len(site_arr), bool)), "aligned_sites": summarise(al),
                                "remove_aligned": summarise(al & (mode_arr == "remove")), "patch_aligned": summarise(al & (mode_arr == "patch")),
                                "remove_all": summarise(mode_arr == "remove"), "patch_all": summarise(mode_arr == "patch"),
                                "by_site": {s: summarise(site_arr == s) for s in sites}}
    return res


def next_weights(kind, W):
    """For the statistics baseline: the weight matrix that reads each site, where there is a single one."""
    if kind == "onelayer_transformer":
        return {"resid_mid": W["W_in"], "mlp_post": W["W_out"], "mlp_out": W["W_U"], "resid_post": W["W_U"], "attn_out": W["W_in"]}
    if kind in ("mlp_tanh", "mlp_relu"):
        return {f"h{k}": W[f"W{k + 1}"] for k in range(1, 9) if f"W{k + 1}" in W}
    return {}


def render(res):
    L = [f"HELD-OUT INTERVENTIONS on {res['target']}: {res['n_interventions_scored']} interventions x {res['n_inputs']} inputs. "
         f"The construction aligns to: {', '.join(res['sites_aligned_by_construction']) or 'nothing'}."]
    for scope, title in (("patch_aligned", "PATCH a subspace from another input, at sites the construction aligns to"),
                         ("remove_aligned", "REMOVE a subspace, at sites the construction aligns to"),
                         ("patch_all", "PATCH, all sites (the construction predicts 'no change' where it has no alignment)"),
                         ("remove_all", "REMOVE, all sites"), ("all_sites", "Everything")):
        L.append(f"\n{title}")
        L.append(f"  {'predictor':14s} {'decision acc':>12s} {'when changed':>13s} {'when unchanged':>15s} {'kept: Spearman':>15s} {'kept: abs err':>14s}")
        for n, p in res["predictors"].items():
            r = p[scope]
            if r is None:
                continue
            f = lambda v, pct=True: "   n/a" if v is None else (f"{v:.1%}" if pct else f"{v:.2f}")      # noqa: E731
            L.append(f"  {n:14s} {f(r['decision_accuracy']):>12s} {f(r['accuracy_when_changed']):>13s} {f(r['accuracy_when_unchanged']):>15s} "
                     f"{f(r['kept_spearman'], False):>15s} {f(r['kept_mae'], False):>14s}")
        any_p = next(iter(res["predictors"].values()))[scope]
        if any_p:
            L.append(f"  (the network's decision changed in {any_p['share_changed']:.1%} of these cases; {any_p['n_interventions']} interventions)")
    L.append("\nDecision accuracy by site, both modes (construction / attribution / statistics / no_change):")
    for s in res["sites"]:
        cells = []
        for n in ("construction", "attribution", "statistics", "no_change"):
            r = res["predictors"][n]["by_site"].get(s)
            cells.append("n/a" if r is None else f"{r['decision_accuracy']:.1%}")
        mark = "" if s in res["sites_aligned_by_construction"] else "   (not aligned by the construction)"
        L.append(f"  {s:13s} " + " / ".join(cells) + mark)
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("target"); ap.add_argument("construction")
    ap.add_argument("--also", action="append", default=[], help="name=path of another construction to score the same way")
    ap.add_argument("--n", type=int, default=40, help="interventions per site")
    ap.add_argument("--json"); ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    also = [(x.split("=", 1)[0], Path(x.split("=", 1)[1]).read_text()) for x in a.also]
    res = run(a.target, Path(a.construction).read_text(), also, a.n, a.seed)
    print(render(res))
    if a.json:
        Path(a.json).write_text(json.dumps(res, indent=1))

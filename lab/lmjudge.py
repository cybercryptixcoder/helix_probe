"""The judge for language-model targets. The construction format and the tests are those of judge.py; what changes
is what a "site" is and what "complete" means in a real, many-position, many-layer model.

UNITS OF TESTING
  * A CUT. All residual-stream sites a construction names at one depth L (resid{L}@p for several positions p) are
    tested together as one unit, "cut{L}". The cut is the state of the computation at depth L: everything the later
    layers can use. Its substitution test replaces the named positions by the construction's prediction AND every
    other position at that depth by its mean over the prompts, so passing means: at depth L the network needs
    nothing that varies with the input except what the construction names there.
  * A COMPONENT site (attn{L}@p, mlp{L}@p, head{L}.{H}@p, neur{L}@p, pattern{L}.{H}@p), tested alone.
Each unit gets the tests of judge.py: alignment (one affine map per site, variables -> activation), substitution,
necessity, compactness, interchange, partial / edit, each next to its controls.

STAGES AND COMPLETENESS
  The depth of the model is divided into stages: the embedding (depth 0), then bands of layers (four bands; for a
  12-layer model 0-2, 3-5, 6-8, 9-11). A stage is explained when a cut inside it is verified (resid{L} for L >= 1
  belongs to the band of layer L - 1, whose output it is). A construction is COMPLETE when it behaves like the
  network and every stage has a verified cut: it then says what the network holds, and where, from the tokens to the
  answer. Component sites add detail (which head or MLP carries a variable) but do not explain a stage alone.

Run:  python3 lab/judge.py <lm target id> <construction.py>      (judge.py dispatches here for LM targets)
"""
import json, sys, time
from pathlib import Path

import numpy as np

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB))
import judge as J  # noqa: E402
import lm          # noqa: E402

N_PAIRS = 300
MAX_TEST = 400
FD_EPS = 2e-2          # step of the finite-difference estimate used for attribution patching (float32 engine)
PCA_KEEP = 0.99        # compactness is measured against the number of principal components that keep this share of answers
MIN_PER_VALUE = 6      # a categorical (one-hot) variable is accepted when each value occurs in this many prompts on average


def categorical(v):
    """Is this variable a one-hot code (the identity of something)? Returns its number of values, or 0."""
    if v.shape[1] < 2 or not (np.isin(v, (0.0, 1.0)).all() and (v.sum(1) == 1).all()):
        return 0
    return int((v.sum(0) > 0).sum())


def stage_names(n_layers):
    w = -(-n_layers // 4)
    bands = [(a, min(a + w, n_layers) - 1) for a in range(0, n_layers, w)]
    return ["embedding"] + [f"layers {a}-{b}" if a != b else f"layer {a}" for a, b in bands], w


def stage_of(what, layer, n_layers):
    names, w = stage_names(n_layers)
    if what == "resid":
        return names[0] if layer == 0 else names[1 + (layer - 1) // w]
    return names[1 + layer // w]


class Unit:
    """One or more sites tested together. For a cut: the named residual positions at one depth."""

    def __init__(self, task, name, sites, kind):
        self.task, self.name, self.sites, self.kind = task, name, sites, kind
        self.widths = [task.width(s) for s in sites]
        self.off = np.concatenate([[0], np.cumsum(self.widths)])
        self.layer = lm.parse_site(sites[0])[1]

    def acts(self, idx):
        if self.kind == "cut":
            return np.concatenate([self.task.resid(self.layer, idx, lm.parse_site(s)[3]) for s in self.sites], 1)
        a = self.task.acts(idx, self.sites)
        return np.concatenate([a[s] for s in self.sites], 1)

    def hook(self, value):
        return {s: value[:, self.off[i]:self.off[i + 1]] for i, s in enumerate(self.sites)}

    def run(self, idx, value):
        return self.task.run(idx, hook=self.hook(value))

    def run_cut(self, idx, value, others):
        """Cut only: named positions <- value, every other position at this depth <- others [T, d] (their mean)."""
        t = self.task
        full = np.broadcast_to(others[None], (len(idx), t.T, others.shape[1])).copy()
        ar = np.arange(len(idx))
        for i, s in enumerate(self.sites):
            p = t.pos(lm.parse_site(s)[3], np.asarray(idx)).numpy()
            full[ar, p] = value[:, self.off[i]:self.off[i + 1]]
        return t.run(idx, hook={f"resid{self.layer}@*": full.reshape(len(idx), -1)})


def judge(tid, source, variant="original", seed=0, n_pairs=N_PAIRS):
    t0 = time.time()
    J.GROUPS = None
    rng = np.random.default_rng(seed)
    task = lm.get_task(tid, variant)
    nL = task.cfg["n_layers"]
    model, align = J.load_construction(source)
    for var, where in align.items():
        for s in where:
            try:
                task.check_site(s)
            except ValueError as e:
                raise J.ConstructionError(f'ALIGN["{var}"]: {e}') from None
            if s.endswith("@*"):
                raise J.ConstructionError(f'ALIGN["{var}"]: "{s}" names every position at once; align a variable to one position (a role or a token index).')
    X, N = task.X, task.N
    allidx = np.arange(N)
    out_n = task.run(allidx)
    out_c, vals = J.run_model(model, X)
    if out_c.shape[1] != out_n.shape[1]:
        raise J.ConstructionError(f"model returns {out_c.shape[1]} outputs per input; the network's output has {out_n.shape[1]} "
                                  f"(the logits of the task's {out_n.shape[1]} answer tokens).")
    for var in align:
        if var not in vals:
            raise J.ConstructionError(f'ALIGN names "{var}", but model never calls iv("{var}", ...). Variables it defines: {", ".join(vals) or "none"}.')
    # fit / test split: by the values of one input column when the task asks for it (so alignments must generalise
    # to values they were not fitted on), otherwise by prompt
    split_by = task.meta.get("split_by")
    if split_by:
        col = X[:, task.meta["x_names"].index(split_by)]
        u = rng.permutation(np.unique(col))
        infit = np.isin(col, u[: len(u) // 2])
        fit, test = allidx[infit], allidx[~infit]
    else:
        perm = rng.permutation(N)
        fit, test = perm[: N // 2], perm[N // 2:]
    if len(test) > MAX_TEST:
        test = rng.choice(test, MAX_TEST, replace=False)

    # a site that is the same for every prompt holds no variable
    def constant(s):
        what, layer, head, pos = lm.parse_site(s)
        a = task.resid(layer, fit[:64], pos) if what == "resid" else task.acts(fit[:64], [s])[s]
        return a.std(0).max() <= 1e-6
    all_sites = sorted({s for where in align.values() for s in where})
    dropped = [s for s in all_sites if constant(s)]
    align = {v: [s for s in where if s not in dropped] for v, where in align.items()}
    align = {v: where for v, where in align.items() if where}

    cats = {v: categorical(vals[v]) for v in vals}
    for v, k in cats.items():
        if k and v in align and N / k < MIN_PER_VALUE:
            raise J.ConstructionError(f'"{v}" is a one-hot code with {k} values over {N} prompts: under {MIN_PER_VALUE} prompts per value, which is '
                                      "a table of the inputs, not a variable. A categorical variable must abstract over the other inputs "
                                      "(the identity of ONE token or quantity); split it into separate variables, or use a compact code.")
    rep = {"target": tid, "kind": "lm", "n_inputs": N, "categorical": {v: k for v, k in cats.items() if k}, "n_fit": len(fit), "n_test": len(test), "source_chars": len(source),
           "variables": {v: {"dim": int(vals[v].shape[1]), "sites": align.get(v, [])} for v in vals},
           "unaligned_variables": [v for v in vals if v not in align], "constant_sites_ignored": dropped}
    const = np.broadcast_to(out_n[fit].mean(0), out_n[test].shape)
    rep["behaviour"] = {"match": J.match(out_c[test], out_n[test]), "r2": J.r2(out_c[test], out_n[test]), "kl": J.kl(out_n[test], out_c[test]),
                        "baseline_constant_match": J.match(const, out_n[test])}

    # units: one cut per depth with residual sites; every other site alone
    units = []
    named = sorted({s for where in align.values() for s in where}, key=lambda s: (lm.parse_site(s)[1], s))
    for L in sorted({lm.parse_site(s)[1] for s in named if lm.parse_site(s)[0] == "resid"}):
        ss = [s for s in named if lm.parse_site(s)[:2] == ("resid", L)]
        units.append(Unit(task, f"cut{L}", ss, "cut"))
    units += [Unit(task, s, [s], "site") for s in named if lm.parse_site(s)[0] != "resid"]

    rep["sites"], rep["interventions"], unit_stage = {}, [], {}
    base = rng.choice(test, n_pairs); src = rng.choice(test, n_pairs)
    clean = out_n[test]
    for u in units:
        names = [v for v in vals if any(s in align.get(v, []) for s in u.sites)]
        cols, k0 = {}, 0
        for v in names:
            cols[v] = np.arange(k0, k0 + vals[v].shape[1]); k0 += vals[v].shape[1]
        V = np.concatenate([vals[v] for v in names], 1)
        K, Wd = V.shape[1], int(u.off[-1])
        A = u.acts(allidx)
        # one affine map per site, from the variables aligned to that site
        c, vmu = A[fit].mean(0), V[fit].mean(0)
        M, D, cnt = np.zeros((K, Wd)), np.zeros((Wd, K)), np.zeros(K)
        for i, s in enumerate(u.sites):
            Jc = np.concatenate([cols[v] for v in names if s in align[v]])
            sl = slice(u.off[i], u.off[i + 1])
            Ms, *_ = np.linalg.lstsq(V[fit][:, Jc] - vmu[Jc], A[fit][:, sl] - c[sl], rcond=1e-8)
            # the read map (a linear probe). The site is wider than the number of fit prompts, so the probe is fitted on
            # the site's leading principal components (a quarter as many as there are fit prompts), not on raw coordinates
            _, svs, Vts = np.linalg.svd(A[fit][:, sl] - c[sl], full_matrices=False)
            rr = max(1, min(int((svs > 1e-6 * max(svs[0], 1e-12)).sum()), max(8, len(fit) // 4)))
            Dz, *_ = np.linalg.lstsq((A[fit][:, sl] - c[sl]) @ Vts[:rr].T, V[fit][:, Jc] - vmu[Jc], rcond=1e-6)
            Ds = Vts[:rr].T @ Dz
            M[Jc, sl] = Ms; D[sl, Jc] = Ds; cnt[Jc] += 1
        D = D / np.maximum(cnt, 1)                       # a variable placed at several sites of the unit: the mean of its read-outs
        A_hat = c + (V - vmu) @ M
        Mp = np.linalg.pinv(M, rcond=1e-8)
        tol = 1e-8 * max(1.0, np.abs(M).max())
        rank = int(np.linalg.matrix_rank(M, tol=tol))
        P = Mp @ M

        def rand_proj(r):
            Q, _ = np.linalg.qr(rng.normal(size=(Wd, r)))
            return Q @ Q.T
        At = A[test]
        if u.kind == "cut":
            others = task.resid(u.layer, fit).mean(0)                               # [T, d]: every position's mean at this depth
            o_splice = u.run_cut(test, A_hat[test], others)
        else:
            o_splice = u.run(test, A_hat[test])
        o_mean = u.run(test, np.broadcast_to(c, At.shape))
        o_keep = u.run(test, c + (At - c) @ P)
        o_excl = u.run(test, At - (At - c) @ P)
        excl_rand = J.match(u.run(test, At - (At - c) @ rand_proj(rank)), clean) if 0 < rank < Wd else None
        m_splice, m_mean = J.match(o_splice, clean), J.match(o_mean, clean)
        # the smallest number of principal components of the unit that keeps 90% of decisions
        _, sv, Vt = np.linalg.svd(A[fit] - c, full_matrices=False)
        full = int((sv > 1e-6 * max(sv[0], 1e-12)).sum())
        lo, hi = 1, max(full, 1)
        ck = f"{tid}|{variant}|{seed}|{','.join(u.sites)}|{PCA_KEEP}"       # this number does not depend on the construction: cached
        cfile = LAB / "runs" / "lm_pca_cache.json"
        cache = json.loads(cfile.read_text()) if cfile.exists() else {}
        if ck in cache:
            lo = hi = cache[ck]
        while lo < hi:
            mid = (lo + hi) // 2
            if J.match(u.run(test, c + (At - c) @ Vt[:mid].T @ Vt[:mid]), clean) >= PCA_KEEP:
                hi = mid
            else:
                lo = mid + 1
        if ck not in cache:
            cache = json.loads(cfile.read_text()) if cfile.exists() else {}
            cache[ck] = int(lo)
            cfile.parent.mkdir(exist_ok=True); cfile.write_text(json.dumps(cache))
        r = {"width": Wd, "variables": names, "named_dims": int(K), "named_rank": rank, "pca_sufficient_rank": int(lo),
             "activation_rank": full, "unit": u.kind, "member_sites": u.sites,
             "explained": float(1 - ((A_hat[test] - At) ** 2).sum() / max(((At - c) ** 2).sum(), 1e-12)),
             "substitute_match": m_splice, "substitute_kl": J.kl(clean, o_splice), "substitute_r2": J.r2(o_splice, clean),
             "mean_ablate_match": m_mean, "recovered": float((m_splice - m_mean) / max(1 - m_mean, 1e-9)),
             "keep_named_match": J.match(o_keep, clean), "remove_named_match": J.match(o_excl, clean), "remove_random_match": excl_rand}
        if u.kind == "cut":
            r["substitute_alone_match"] = J.match(u.run(test, A_hat[test]), clean)      # other positions left as they are
        rep["sites"][u.name] = r
        unit_stage[u.name] = stage_of("resid" if u.kind == "cut" else lm.parse_site(u.sites[0])[0], u.layer, nL)

        dA = (A[src] - A[base]) @ D
        tests = [("interchange", names, None)]
        if len(names) > 1:
            tests += [("partial", [v], None) for v in names]
        if K >= 2 and not all(cats[v] for v in names):       # a one-hot code has no separable coordinates to edit
            tests.append(("edit", names, "half"))
        live = []
        for mode, vs, how in tests:
            Jc = np.concatenate([cols[v] for v in vs])
            mask = np.ones((n_pairs, len(Jc)))
            if how == "half":
                mask = (rng.random((n_pairs, len(Jc))) < 0.5).astype(float)
                dead = mask.sum(1) == 0
                mask[dead, rng.integers(0, len(Jc), dead.sum())] = 1
                full_ = mask.sum(1) == len(Jc)
                mask[full_, rng.integers(0, len(Jc), full_.sum())] = 0
            new_all = V[base].copy()
            new_all[:, Jc] = np.where(mask > 0, V[src][:, Jc], V[base][:, Jc])
            o_pred, _ = J.run_model(model, X[base], {v: new_all[:, cols[v]] for v in vs})
            delta = (new_all[:, Jc] - V[base][:, Jc]) @ M[Jc] if mode == "edit" else dA[:, Jc] @ M[Jc]
            o_net = u.run(base, A[base] + delta)
            controls = mode == "interchange"          # the two costly controls are run on the interchange test only
            if controls:
                o_lin = out_n[base] + (u.run(base, A[base] + FD_EPS * delta) - out_n[base]) / FD_EPS
                rk = max(1, int(np.linalg.matrix_rank(M[Jc], tol=tol)))
                o_rand = u.run(base, A[base] + (A[src] - A[base]) @ rand_proj(min(rk, Wd)))
            changed = ~J.same(o_net, out_n[base])
            agree = J.same(o_pred, o_net)
            rep["interventions"].append({
                "variable": vs[0] if len(vs) == 1 else "all variables", "variables": vs, "site": u.name, "mode": mode, "dim": int(len(Jc)),
                "agreement": float(agree.mean()), "r2": J.r2(o_pred, o_net), "network_changed": float(changed.mean()),
                "agreement_when_changed": float(agree[changed].mean()) if changed.any() else None,
                "baseline_no_change": J.match(out_n[base], o_net), "baseline_source_output": J.match(out_n[src], o_net),
                "control_random_subspace": J.match(o_pred, o_rand) if controls else None,
                "attribution_patching": float(J.same(o_lin, o_net).mean()) if controls else None,
                "attribution_patching_when_changed": float(J.same(o_lin, o_net)[changed].mean()) if controls and changed.any() else None})
            if len(vs) == 1 and changed.mean() >= 0.05:
                live.append(vs[0])
        live = [v for v in names if v in live]
        # size: categorical variables (identities) are exempt; the rest is compared with the principal components that suffice
        sized = [v for v in live if not cats[v]]
        Jl = np.concatenate([cols[v] for v in sized]) if sized else np.array([], int)
        r["used_rank"] = int(np.linalg.matrix_rank(M[Jl], tol=tol)) if len(Jl) else 0
        r["categorical"] = {v: cats[v] for v in names if cats[v]}
        r["unused_variables"] = [v for v in names if v not in live]

    names_, _ = stage_names(nL)
    w = -(-nL // 4)
    rep["stages"] = {}
    for i, nm in enumerate(names_):
        where = ["resid0 (token + position embeddings)"] if i == 0 else [f"resid{L}" for L in range((i - 1) * w + 1, min(i * w, nL) + 1)]
        rep["stages"][nm] = {"sites": where, "named": [], "verified": []}
    rep["uncovered_sites"] = []
    rep["verdict"] = v = J.verdict(rep)
    rep["components_verified"] = []
    for name, r in rep["sites"].items():
        if r["unit"] == "cut":
            st = rep["stages"][unit_stage[name]]
            st["named"].append(name)
            if r["pass"]:
                st["verified"].append(name)
        elif r["pass"]:
            rep["components_verified"].append(name)
    v["stages_total"] = len(rep["stages"])
    v["stages_verified"] = sum(bool(st["verified"]) for st in rep["stages"].values())
    v["complete"] = bool(v["verified"] and v["stages_verified"] == v["stages_total"])
    v["score"] = round(rep["behaviour"]["match"] * v["stages_verified"] / max(1, v["stages_total"]), 4)
    rep["seconds"] = round(time.time() - t0, 2)
    return rep


def render(rep):
    import copy
    rep2 = copy.deepcopy(rep)
    for t in rep2["interventions"]:
        for k in ("control_random_subspace", "attribution_patching"):
            if t[k] is None:
                t[k] = float("nan")
    text = J.render(rep2).replace("random subspace nan%, ", "").replace(", attribution patching nan%", "")
    notes = []
    if rep.get("categorical"):
        notes.append("Categorical (one-hot) variables, exempt from the size limit: " + ", ".join(f"{v} ({k} values)" for v, k in rep["categorical"].items()))
    notes += ["UNITS  cutL = every residual site you named at depth L (resid{L}@...), tested together. Its 'substitute' number replaces "
             "the named positions by your prediction AND every other position at that depth by its mean: the cut must hold everything "
             "the later layers need. Sites of other kinds (attn, mlp, head, neur, pattern) are tested alone; they add detail but only a "
             "verified cut explains a stage."]
    for name, r in rep["sites"].items():
        if r.get("unit") == "cut":
            notes.append(f"  {name} = {', '.join(r['member_sites'])}: substitute {r['substitute_match']:.1%} with the other positions set to "
                         f"their mean ({r['substitute_alone_match']:.1%} with the other positions left as they are)")
    if rep.get("components_verified"):
        notes.append("Verified component sites: " + ", ".join(rep["components_verified"]))
    lines = text.split("\n")
    k = next(i for i, l in enumerate(lines) if l.startswith("4. INTERVENTIONS"))
    return "\n".join(lines[:k] + notes + lines[k:])


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("target"); ap.add_argument("construction")
    ap.add_argument("--variant", default="original"); ap.add_argument("--json"); ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    try:
        rep = judge(a.target, Path(a.construction).read_text(), a.variant, a.seed)
    except J.ConstructionError as e:
        print("CONSTRUCTION ERROR:", e); sys.exit(1)
    print(render(rep))
    if a.json:
        Path(a.json).write_text(json.dumps(rep, indent=1))

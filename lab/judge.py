"""The judge: tests a construction against a network. The same tests for every network; nothing here knows any task.

A CONSTRUCTION is a small, standalone Python file with two things in it:

    def model(x, iv):
        # x: the inputs, an array [B, n_in]. Returns the predicted network output, an array [B, n_out].
        # Every named intermediate variable goes through iv:   v = iv("name", value)   with value shaped [B] or [B, k].
        # iv returns the value to use from then on, in the same shape (during an intervention test it returns a
        # replaced value), so later steps must be computed from what iv returned.

    ALIGN = {"name": ["site", ...], ...}     # where in the network each variable lives (site names: nets.site_table)

The file may use numpy (np) and math, and nothing else: it cannot see the weights. Its length is its description length.

The judge measures, on inputs held out from fitting:
  1. BEHAVIOUR      run the construction in place of the network: do the outputs agree?
  2. ALIGNMENT      at each site named in ALIGN, fit one affine map from the variables to the activations
                    (activation ~ c + variables @ M; this declared, restricted map is the alignment) and report how
                    much of the activation it explains.
  3. SUBSTITUTION   replace the site's activation with the construction's prediction (c + variables @ M) and run the
                    rest of the network ("keep only what it names"); also project the real activation onto the named
                    subspace; also remove the named subspace ("remove only what it names"), against a random subspace
                    of the same size and against mean-ablating the whole site.
  4. INTERVENTION   interchange: copy a variable's subspace from a source input's run into a base input's run, and
                    compare the network's new output with what the construction predicts when that variable is set to
                    its source value. Also a stricter edit: give a random half of the variable's coordinates the values
                    they have on the source input (a state no real input produces), written into the network along the
                    variable's fitted directions, and compare with the construction's prediction for that edited state.
                    Controls: the same test with a random subspace; predicting "no change"; predicting the source output.

Run:  python3 lab/judge.py <target id> <construction.py> [--variant original|shuffled|untrained|permuted] [--json out.json]
"""
import json, math, sys, time, traceback
from pathlib import Path

import numpy as np

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB))
import nets  # noqa: E402

MAX_SOURCE_CHARS = 16000
PASS = {"behaviour": 0.95, "substitution": 0.90, "interchange": 0.90, "edit": 0.50, "removal_gap": 0.5}


class ConstructionError(Exception):
    pass


# ---------------------------------------------------------------- loading and running a construction
def load_construction(source):
    if len(source) > MAX_SOURCE_CHARS:
        raise ConstructionError(f"The construction is {len(source):,} characters; the limit is {MAX_SOURCE_CHARS:,}. "
                                "A construction is a compact program, not a table of the network's values.")
    import builtins
    real_import = builtins.__import__

    def guarded(name, globals=None, locals=None, fromlist=(), level=0):
        if (globals or {}).get("__name__") == "__construction__" and name.split(".")[0] not in ("numpy", "math", "itertools", "functools"):
            raise ImportError(f"a construction may import only numpy and math, not '{name}'")
        return real_import(name, globals, locals, fromlist, level)

    env = {"__name__": "__construction__", "np": np, "math": math}
    builtins.__import__ = guarded
    try:
        exec(compile(source, "<construction>", "exec"), env)
    except Exception as e:  # noqa: BLE001
        raise ConstructionError("The construction file did not run:\n" + _short_tb()) from e
    finally:
        builtins.__import__ = real_import
    if not callable(env.get("model")):
        raise ConstructionError("The construction must define  def model(x, iv): ...")
    align = env.get("ALIGN")
    if not isinstance(align, dict) or not align:
        raise ConstructionError('The construction must define  ALIGN = {"variable name": ["site", ...], ...}  with at least one variable.')
    align = {str(k): ([v] if isinstance(v, str) else list(v)) for k, v in align.items()}
    return env["model"], align


def _short_tb():
    lines = traceback.format_exc().splitlines()
    keep = [l for l in lines if "judge.py" not in l]
    return "\n".join(keep[-12:])


def run_model(model, X, overrides=None):
    """Run the construction on inputs X. overrides: {variable: array [B, k]} replaces those variables' values.
    Returns (output [B, n_out], {variable: value as computed before any override})."""
    values = {}

    def iv(name, value):
        v = np.asarray(value, dtype=np.float64)
        if v.ndim == 1:
            v = v[:, None]
        if v.ndim != 2 or v.shape[0] != len(X):
            raise ConstructionError(f'iv("{name}", value): value must be shaped [B, k] with B = {len(X)}; got {v.shape}.')
        if name in values:
            raise ConstructionError(f'iv("{name}", ...) was called twice; each variable is defined once.')
        values[name] = v
        if overrides and name in overrides:
            v = np.asarray(overrides[name], dtype=np.float64).reshape(v.shape)
        return v[:, 0] if np.ndim(value) == 1 else v.copy()     # same shape as it was given

    try:
        out = np.asarray(model(np.array(X), iv), dtype=np.float64)
    except ConstructionError:
        raise
    except Exception as e:  # noqa: BLE001
        raise ConstructionError("model(x, iv) raised an error:\n" + _short_tb()) from e
    if out.ndim == 1:
        out = out[:, None]
    if out.shape[0] != len(X):
        raise ConstructionError(f"model must return [B, n_out] with B = {len(X)}; got {out.shape}.")
    if not np.isfinite(out).all():
        raise ConstructionError("model returned NaN or infinite values.")
    return out, values


# ---------------------------------------------------------------- comparing outputs
def decide(out):
    """The network's decision for each input: the largest output, or the sign when there is one output."""
    return out.argmax(-1) if out.shape[1] > 1 else (out[:, 0] > 0).astype(int)


def match(a, b):
    return float((decide(a) == decide(b)).mean())


def r2(pred, true):
    """Share of variance explained. Multi-output values are compared after removing each row's mean (logits are only
    defined up to a constant per input)."""
    if true.shape[1] > 1 and pred.shape == true.shape:
        pred, true = pred - pred.mean(1, keepdims=True), true - true.mean(1, keepdims=True)
    sst = ((true - true.mean(0)) ** 2).sum()
    return float(1 - ((pred - true) ** 2).sum() / max(sst, 1e-12))


def kl(net, other):
    """Mean KL(network's distribution || other's) for multi-output networks; None for one output."""
    if net.shape[1] == 1:
        return None
    def lsm(z):
        z = z - z.max(-1, keepdims=True)
        return z - np.log(np.exp(z).sum(-1, keepdims=True))
    p, q = lsm(net), lsm(other)
    return float((np.exp(p) * (p - q)).sum(-1).mean())


# ---------------------------------------------------------------- the tests
def judge(kind, W, X, source, seed=0, n_pairs=2000):
    """Returns a report dict. Raises ConstructionError with a message the author can act on."""
    t0 = time.time()
    rng = np.random.default_rng(seed)
    model, align = load_construction(source)
    table = nets.site_table(kind, W)
    sites = {name: width for name, width, _, _ in table}
    stage_of = {name: stage for name, _, _, stage in table}
    for var, where in align.items():
        for s in where:
            if s not in sites:
                raise ConstructionError(f'ALIGN["{var}"] names site "{s}", which this network does not have. Sites: {", ".join(sites)}.')
            if s == "out":
                raise ConstructionError('ALIGN cannot use the site "out": the output is what model() returns. Align variables to internal sites.')
    X = np.asarray(X)
    N = len(X)
    acts = {}
    out_n = nets.forward(kind, W, X, acts=acts)
    out_c, vals = run_model(model, X)
    if out_c.shape[1] != out_n.shape[1]:
        raise ConstructionError(f"model returns {out_c.shape[1]} outputs per input; the network has {out_n.shape[1]}.")
    for var in align:
        if var not in vals:
            raise ConstructionError(f'ALIGN names "{var}", but model never calls iv("{var}", ...). Variables it defines: {", ".join(vals) or "none"}.')
    if N >= 200:
        perm = rng.permutation(N)
        fit, test = perm[: N // 2], perm[N // 2:]
    else:
        fit = test = np.arange(N)

    rep = {"n_inputs": N, "n_fit": len(fit), "n_test": len(test), "source_chars": len(source),
           "variables": {v: {"dim": int(vals[v].shape[1]), "sites": align.get(v, [])} for v in vals},
           "unaligned_variables": [v for v in vals if v not in align]}

    # 1. behaviour
    const = np.broadcast_to(out_n[fit].mean(0), out_n[test].shape)
    rep["behaviour"] = {"match": match(out_c[test], out_n[test]), "r2": r2(out_c[test], out_n[test]), "kl": kl(out_n[test], out_c[test]),
                        "baseline_constant_match": match(const, out_n[test])}

    # 2-4. per site
    rep["sites"], rep["interventions"] = {}, []
    base = rng.choice(test, n_pairs); src = rng.choice(test, n_pairs)
    out_c_base = out_c[base]
    for s in [s for s in sites if any(s in w for w in align.values())]:
        names = [v for v in vals if s in align.get(v, [])]
        cols, k0 = {}, 0
        for v in names:
            cols[v] = np.arange(k0, k0 + vals[v].shape[1]); k0 += vals[v].shape[1]
        V = np.concatenate([vals[v] for v in names], 1)
        A = acts[s]
        vmu, c = V[fit].mean(0), A[fit].mean(0)
        M, *_ = np.linalg.lstsq(V[fit] - vmu, A[fit] - c, rcond=1e-8)          # [K, d]
        A_hat = c + (V - vmu) @ M
        Mp = np.linalg.pinv(M, rcond=1e-8)                                      # [d, K]: activation -> variable coordinates
        rank = int(np.linalg.matrix_rank(M, tol=1e-8 * max(1.0, np.abs(M).max())))
        P = Mp @ M                                                              # projector onto the named subspace
        def run(hook_value, idx=test):
            return nets.forward(kind, W, X[idx], hook={s: hook_value})
        def rand_proj(r):
            Q, _ = np.linalg.qr(rng.normal(size=(A.shape[1], r)))
            return Q @ Q.T
        clean = out_n[test]
        o_splice = run(A_hat[test])
        o_mean = run(np.broadcast_to(c, A[test].shape))
        o_keep = run(c + (A[test] - c) @ P)
        o_excl = run(A[test] - (A[test] - c) @ P)
        excl_rand = float(np.mean([match(run(A[test] - (A[test] - c) @ rand_proj(rank)), clean) for _ in range(3)])) if 0 < rank < A.shape[1] else None
        m_splice, m_mean = match(o_splice, clean), match(o_mean, clean)
        rep["sites"][s] = {
            "width": int(A.shape[1]), "variables": names, "named_dims": int(V.shape[1]), "named_rank": rank,
            "explained": float(1 - ((A_hat[test] - A[test]) ** 2).sum() / max(((A[test] - c) ** 2).sum(), 1e-12)),
            "substitute_match": m_splice, "substitute_kl": kl(clean, o_splice), "substitute_r2": r2(o_splice, clean),
            "mean_ablate_match": m_mean,
            "recovered": float((m_splice - m_mean) / max(1 - m_mean, 1e-9)),
            "keep_named_match": match(o_keep, clean), "remove_named_match": match(o_excl, clean), "remove_random_match": excl_rand,
        }
        # interventions on each variable at this site
        # interchange reads each variable from the real activations with the best linear probe (fit on the fit split)
        D, *_ = np.linalg.lstsq(A[fit] - c, V[fit] - vmu, rcond=1e-6)           # [d, K]: activation -> variable values
        dA = (A[src] - A[base]) @ D                                             # the change in every variable, as read from the two runs
        for v in names:
            J = cols[v]
            for mode in (["interchange", "edit"] if len(J) >= 2 else ["interchange"]):
                mask = np.ones((n_pairs, len(J)))
                if mode == "edit":
                    mask = (rng.random((n_pairs, len(J))) < 0.5).astype(float)
                    dead = mask.sum(1) == 0
                    mask[dead, rng.integers(0, len(J), dead.sum())] = 1
                    full = mask.sum(1) == len(J)
                    mask[full, rng.integers(0, len(J), full.sum())] = 0
                new_val = np.where(mask > 0, vals[v][src], vals[v][base])
                o_pred, _ = run_model(model, X[base], {v: new_val})
                if mode == "interchange":      # copy the variable's coordinates as read from the source run's activation
                    delta = dA[:, J] @ M[J]
                else:                          # write the construction's own new value along the variable's fitted directions
                    delta = (new_val - vals[v][base]) @ M[J]
                o_net = nets.forward(kind, W, X[base], hook={s: A[base] + delta})
                r = max(1, int(np.linalg.matrix_rank(M[J], tol=1e-8 * max(1.0, np.abs(M).max()))))
                Pr = rand_proj(min(r, A.shape[1]))
                o_rand = nets.forward(kind, W, X[base], hook={s: A[base] + (A[src] - A[base]) @ Pr})
                net_changed = decide(o_net) != decide(out_n[base])
                agree = decide(o_pred) == decide(o_net)
                rep["interventions"].append({
                    "variable": v, "site": s, "mode": mode, "dim": int(len(J)),
                    "agreement": float(agree.mean()),
                    "r2": r2(o_pred, o_net),
                    "network_changed": float(net_changed.mean()),
                    "agreement_when_changed": float(agree[net_changed].mean()) if net_changed.any() else None,
                    "baseline_no_change": match(out_n[base], o_net),
                    "baseline_source_output": match(out_n[src], o_net),
                    "control_random_subspace": match(o_pred, o_rand),
                })
    varying = {s for s in sites if acts[s].std(0).max() > 1e-9}                 # a site that never changes needs no explanation
    rep["uncovered_sites"] = [s for s in sites if s != "out" and s in varying and s not in rep["sites"]]
    rep["stages"] = {}
    for s in sites:
        if s != "out" and s in varying:
            rep["stages"].setdefault(stage_of[s], {"sites": [], "named": [], "verified": []})["sites"].append(s)
    rep["verdict"] = verdict(rep)
    for s, r in rep["sites"].items():
        st = rep["stages"][stage_of[s]]
        st["named"].append(s)
        if r["pass"]:
            st["verified"].append(s)
    v = rep["verdict"]
    v["stages_total"] = len(rep["stages"])
    v["stages_verified"] = sum(bool(st["verified"]) for st in rep["stages"].values())
    v["complete"] = bool(v["verified"] and v["stages_verified"] == v["stages_total"])
    v["score"] = round(rep["behaviour"]["match"] * v["stages_verified"] / max(1, v["stages_total"]), 4)
    rep["seconds"] = round(time.time() - t0, 2)
    return rep


def verdict(rep):
    """A site is VERIFIED when it can be replaced by the construction's prediction, removing what the construction
    names there does damage that removing a random subspace does not, and the construction's predictions about
    interchange interventions and edits on every variable there hold. A construction is VERIFIED when it behaves
    like the network and every site it names is verified, and COMPLETE when, in addition, every stage of the
    network has a verified site. The thresholds are PASS (top of this file)."""
    fails = []
    b = rep["behaviour"]
    if b["match"] < PASS["behaviour"]:
        fails.append(f"behaviour: the construction's output agrees with the network on {b['match']:.1%} of inputs (need {PASS['behaviour']:.0%})")
    for s, r in rep["sites"].items():
        mine = []
        if r["substitute_match"] < PASS["substitution"]:
            mine.append(f"substitution at {s}: {r['substitute_match']:.1%} (need {PASS['substitution']:.0%})")
        if r["remove_random_match"] is not None and r["remove_random_match"] - r["remove_named_match"] < PASS["removal_gap"]:
            mine.append(f"removal at {s}: removing the named subspace leaves {r['remove_named_match']:.1%}, a random subspace of the same "
                        f"size leaves {r['remove_random_match']:.1%} (the named subspace should matter much more: name fewer, more specific dimensions)")
        for t in rep["interventions"]:
            if t["site"] != s:
                continue
            score = t["agreement_when_changed"] if t["agreement_when_changed"] is not None else t["agreement"]
            if t["network_changed"] < 0.05 and t["agreement"] >= 0.95:
                t["pass"] = True        # the construction correctly predicts that this variable is inert at this site
            elif t["network_changed"] < 0.05:
                t["pass"] = False
                mine.append(f"{t['mode']} of {t['variable']} at {s}: the network's output changed in only {t['network_changed']:.1%} of cases, but "
                            "the construction predicted changes: at this site the network's output does not depend on this variable")
            elif t["mode"] == "edit":
                t["pass"] = bool(score >= PASS["edit"] and score >= 2 * t["control_random_subspace"])
                if not t["pass"]:
                    mine.append(f"edit of {t['variable']} at {s}: prediction right in {score:.1%} of the cases where the network's output "
                                f"changed (need {PASS['edit']:.0%} and twice the random-subspace control, {t['control_random_subspace']:.1%})")
            else:
                t["pass"] = bool(score >= PASS["interchange"])
                if not t["pass"]:
                    mine.append(f"interchange of {t['variable']} at {s}: prediction right in {score:.1%} of the cases where the network's "
                                f"output changed (need {PASS['interchange']:.0%})")
        r["pass"] = not mine
        fails += mine
    if not rep["sites"]:
        fails.append("no sites aligned")
    return {"verified": not fails, "fails": fails}


# ---------------------------------------------------------------- text report (what the constructor's reader sees)
def render(rep):
    L = []
    b = rep["behaviour"]
    L.append(f"JUDGE REPORT   ({rep['n_test']} held-out inputs; construction {rep['source_chars']:,} chars)")
    L.append(f"1. BEHAVIOUR  construction vs network output: same decision on {b['match']:.1%} of inputs "
             f"(a constant output would get {b['baseline_constant_match']:.1%}); output R2 {b['r2']:.3f}"
             + (f"; KL {b['kl']:.3f}" if b["kl"] is not None else ""))
    L.append("2-3. SITES   explained = share of the activation's variance the variables explain;  substitute = network decision kept "
             "when the activation is replaced by the construction's prediction;  keep = when only the named subspace of the real "
             "activation is kept;  remove = when the named subspace is removed (should be LOW) vs a random subspace of equal size;  "
             "mean-ablate = when the whole site is replaced by its mean")
    for s, r in rep["sites"].items():
        rr = "n/a" if r["remove_random_match"] is None else f"{r['remove_random_match']:.1%}"
        L.append(f"  {s:11s} ({r['named_rank']}/{r['width']} dims; {', '.join(r['variables'])}): explained {r['explained']:.3f} | "
                 f"substitute {r['substitute_match']:.1%} | keep {r['keep_named_match']:.1%} | remove {r['remove_named_match']:.1%} "
                 f"(random {rr}) | mean-ablate {r['mean_ablate_match']:.1%}")
    L.append("4. INTERVENTIONS   interchange = the variable is copied from another input's run; edit = a random half of its "
             "coordinates are set to another input's values (a state no input produces). right = the construction predicted the network's new decision (all cases / cases where the "
             "decision changed).  controls: the same swap in a random subspace; guessing 'no change'; guessing the source input's output")
    for t in rep["interventions"]:
        w = "n/a" if t["agreement_when_changed"] is None else f"{t['agreement_when_changed']:.1%}"
        L.append(f"  {t['mode']:11s} {t['variable']} @ {t['site']}: right {t['agreement']:.1%} / {w} when changed (network changed in "
                 f"{t['network_changed']:.1%}); output R2 {t['r2']:.3f} | controls: random subspace {t['control_random_subspace']:.1%}, "
                 f"no-change {t['baseline_no_change']:.1%}, source-output {t['baseline_source_output']:.1%}")
    if rep["unaligned_variables"]:
        L.append("Variables in model() with no site in ALIGN (not tested): " + ", ".join(rep["unaligned_variables"]))
    L.append("STAGES   " + ";  ".join(
        f"{name}: " + ("VERIFIED at " + ", ".join(st["verified"]) if st["verified"] else
                       ("named but failing" if st["named"] else "NOT EXPLAINED (no variable at " + " / ".join(st["sites"]) + ")"))
        for name, st in rep["stages"].items()))
    v = rep["verdict"]
    if v["complete"]:
        L.append("VERDICT: VERIFIED AND COMPLETE: every stage of the network has a verified site.")
    elif v["verified"]:
        L.append(f"VERDICT: VERIFIED at every site it names, but INCOMPLETE: {v['stages_verified']} of {v['stages_total']} stages explained.")
    else:
        L.append(f"VERDICT: NOT VERIFIED ({v['stages_verified']} of {v['stages_total']} stages verified). Failing:")
    L += [f"  - {f}" for f in v["fails"]]
    return "\n".join(L)


def load_target(tid, variant="original", seed=0):
    meta = json.loads((LAB / "models" / tid / "meta.json").read_text())
    W = dict(np.load(LAB / "models" / tid / "weights.npz"))
    W = {k: v.astype(np.float64) for k, v in nets.variant(W, variant, meta.get("perm_groups", []), seed).items()}
    return meta, W, nets.domain_inputs(meta)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("target"); ap.add_argument("construction")
    ap.add_argument("--variant", default="original"); ap.add_argument("--json"); ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    meta, W, X = load_target(a.target, a.variant)
    try:
        rep = judge(meta["forward"], W, X, Path(a.construction).read_text(), seed=a.seed)
    except ConstructionError as e:
        print("CONSTRUCTION ERROR:", e); sys.exit(1)
    print(render(rep))
    if a.json:
        Path(a.json).write_text(json.dumps(rep, indent=1))

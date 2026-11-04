import math

def predict(probe):
    # f(x) = 16.8*|x| + r(x) [E1, E2, E4, E6, E7]
    # r(x) is NOT deterministic: repeated probes at same x give different y [E18]
    #   e.g. x=-0.5: 8.2049 (E14), 8.6349 (E15), 8.5089 (E18) -- all different
    #   x=0.3: 6.0561 (E14), 6.7832 (E15), 4.1615 (E18) -- all different
    # So r(x) is noise with a distribution whose mean/scale depends on x.
    # Mean of r(x) appears near 0 for small |x| (base 16.8|x| dominates) [E5,E8,E9,E10,E14-E18]
    # Noise amplitude is roughly constant-ish at small |x| (~1-2), grows slowly with |x| [E6,E7]
    # At large |x| residual amplitude grows ~sqrt(|x|) [E6, E7]
    # No reliable sign asymmetry: differences are within noise [E18 vs E14/E15]
    # Best deterministic prediction = base + expected value of noise (≈0)
    # Use a small deterministic wobble as a placeholder mean; keep it tiny.
    out = []
    for x in probe.get("x", []):
        try:
            ax = abs(x)
            base = 16.8 * ax
            # mean of residual: near zero, slight slow structure (guess)
            mean_r = 0.3 * math.sin(0.5 * x)
            out.append(base + mean_r)
        except Exception:
            out.append(None)
    return {"y": out}

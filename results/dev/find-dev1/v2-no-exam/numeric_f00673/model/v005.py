import math

def predict(probe):
    # f(x) = 16.8*|x| + r(x) [E1, E2, E4, E6, E7]
    # r(x) is NOISY: same x gives different y across calls [E18, E19]
    #   E19: two identical blocks in one session differ (e.g. x=-1.2: 19.3292 vs 19.0536)
    #   E14 vs E19 at x=-1.2: 19.3489 vs 19.3292/19.0536 -- all different
    # So r(x) = deterministic mean + random noise; we predict the mean.
    # Residual mean near 0 at small |x| (base dominates) [E5,E8,E9,E10,E14-E19]
    # Noise scale ~1-2 at small |x|, grows slowly with |x| [E6,E7]
    # No reliable sign asymmetry beyond noise [E18, E19]
    # Best deterministic prediction = 16.8*|x| (mean of noise ~ 0).
    out = []
    for x in probe.get("x", []):
        try:
            out.append(16.8 * abs(x))
        except Exception:
            out.append(None)
    return {"y": out}

import math

def predict(probe):
    # Observations:
    # - Outputs are small, roughly in [-3, 3], with sign changing irregularly.
    # - No obvious monotonic trend across x in E2.
    # - E1 and E2 values look like a smooth-ish but non-periodic function of x.
    # - Values at x=0: E2 gives 0.8711. Nearby x=-5 -> -1.1356, x=5 -> -0.012.
    # - Looks like some combination of sinusoids / polynomial / noise.
    # Best guess: f(x) = a*sin(b*x + c) + d*sin(e*x + f) + small noise? Hard to fit.
    # Without more data, use a simple smooth interpolant-like guess: a low-amplitude
    # combination of sin terms. Mark as uncertain.
    # ? This is a rough guess; the true function is unknown.
    out = []
    for x in probe.get("x", []):
        try:
            v = 1.2*math.sin(0.07*x + 0.3) + 0.9*math.sin(0.13*x + 1.1) + 0.4*math.cos(0.31*x)
            out.append(round(v, 4))
        except Exception:
            out.append(None)
    return {"y": out}

import math

def predict(probe):
    # Observations are roughly in [-0.16, 0.17], look like a smooth oscillatory
    # function of x with no obvious special interval (values near 0 are small,
    # not discontinuous). Best guess: a damped/decaying sinusoid or sinc-like
    # wave. Fit is very rough; marked with "?".
    # E1: y at x=88.2 ~ -0.0006, x=66 ~ 0.0834, x=72.7 ~ 0.0095, x=-61.7 ~ -0.0012
    # E2: y at x=-128 ~ 0.0046, x=-64 ~ 0.1088, x=0 ~ -0.0343, x=32 ~ -0.0856
    # The amplitude does not clearly decay with |x| (x=-64 gives 0.1088, larger
    # than near 0), so a pure decaying wave is wrong. Try a sinusoid in x with
    # some frequency plus a small offset.
    # ? crude guess: y ~ A*sin(w*x + p) with A~0.1, w~0.05, p~0
    out = []
    for x in probe["x"]:
        try:
            y = 0.1 * math.sin(0.05 * x)
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

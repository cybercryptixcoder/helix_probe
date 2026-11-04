import math

def predict(probe):
    # Model of f(x):
    # - There is a central plateau region |x| < ~1 where f is a mild, slowly varying
    #   negative function (roughly -11.7 near 0, drifting to about -7.4 at x=-1 and
    #   about -41.7 at x=+1) [E3, E5, E9].
    # - Outside the plateau, on the positive side (x >= ~1), f grows like a clean
    #   exponential a*b^x. Fit from large positive values: f(64)=-20915544,
    #   f(48)=-6699915.2, f(32)=-1355761.6, f(16)=-90763.2. Ratio per unit x:
    #   b = (20915544/1355761.6)^(1/32) ~ 1.0886; a ~ -41.7/ b^1 ... [E8, E6, E7]
    # - On the negative side (x <= ~-1), f also grows exponentially as x decreases,
    #   i.e. f ~ -A * c^(-x) with c>1. From f(-80)=-47610123.7, f(-64)=-19342450.1,
    #   f(-50)=-7122681.7, f(-40)=-2878507.7: c ~ 1.0886 too (same base) [E10, E1].
    # - The plateau and the two exponential branches meet near |x|=1 with a smooth
    #   transition; the plateau value near x=±1 is about -7.4 (neg) and -41.7 (pos).
    # - f(0) ~ 472.73 is an outlier spike at exactly 0 [E1]; treat as special.
    #
    # Concretely: use exponential branches for |x|>=1, and a smooth interpolation
    # across the plateau for |x|<1.

    # Base of the exponential (same on both sides) [E8, E10]
    b = 1.0886

    # Positive branch: f(x) = a_pos * b^x for x >= 1.
    # Anchor at x=1: f(1) = -41.7  => a_pos = -41.7 / b
    a_pos = -41.7 / b

    # Negative branch: f(x) = a_neg * b^(-x) for x <= -1.
    # Anchor at x=-1: f(-1) = -7.4 => a_neg * b = -7.4 => a_neg = -7.4 / b
    a_neg = -7.4 / b

    # Plateau endpoints
    p_neg = -7.4    # f(-1)
    p_pos = -41.7   # f(1)

    def f(x):
        if x == 0:
            return 472.73  # spike at exactly 0 [E1]
        if x >= 1:
            return a_pos * (b ** x)
        if x <= -1:
            return a_neg * (b ** (-x))
        # Plateau region -1 < x < 1: smooth monotone interpolation between
        # f(-1)=-7.4 and f(1)=-41.7, with mild curvature.
        # Use a smooth blend; near 0 value ~ -11.7 [E5, E9].
        # Linear-ish in the middle but steeper near +1.
        t = (x + 1.0) / 2.0  # 0 at x=-1, 1 at x=1
        # blend with slight ease-in toward positive end
        return p_neg + (p_pos - p_neg) * (t ** 1.6)

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(f(float(x)))
        except Exception:
            ys.append(None)
    return {"y": ys}

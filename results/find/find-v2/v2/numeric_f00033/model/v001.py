import math

def predict(probe):
    # Observations: outputs are tiny except near x=0 where a bump appears.
    # E1: x=2.9 -> 0.0362 (large), x=-6.0 -> 0.0, x=-20.3 -> -0.0013, x=21.3 -> -0.0005
    # E1: x=88.2 -> -0.0002, x=66.0 -> -0.0003, x=-61.7 -> -0.0032, x=-50.4 -> -0.0032
    # Pattern: a narrow Gaussian-like bump centered near x~0 (peak ~0.036 at x=2.9),
    # plus a small negative baseline that grows with |x| slightly.
    # Model: y = A*exp(-((x-mu)/s)^2) + b, with a small negative offset.
    # A ~ 0.04, mu ~ 2.9, s ~ 3 (bump dies by x=-6 and x=21).
    # Baseline: near 0 for large positive, ~-0.003 for large negative.
    # Use a smooth baseline: b(x) = -0.003 * sigmoid(-(x)/20) roughly.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            bump = 0.04 * math.exp(-((x - 2.9) / 3.0) ** 2)
            base = -0.003 / (1.0 + math.exp(x / 15.0))
            ys.append(bump + base)
        except Exception:
            ys.append(None)
    return {"y": ys}

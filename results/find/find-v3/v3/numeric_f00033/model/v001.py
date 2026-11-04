import math

def predict(probe):
    # Observations [E1]:
    # - Outputs are tiny except near x=0.
    # - x=2.9 -> 0.0362 (largest), x=-6.0 -> 0.0, x=-20.3 -> -0.0013,
    #   x=-24.3 -> -0.0016, x=-50.4 -> -0.0032, x=-61.7 -> -0.0032,
    #   x=21.3 -> -0.0005, x=66.0 -> -0.0003, x=72.7 -> -0.0003, x=88.2 -> -0.0002.
    # - Shape: peaked positive bump near x~3, negative dip for x<0 that
    #   saturates around -0.003, near-zero for large positive x.
    # Hypothesis (?): f(x) = A*x*exp(-x^2/(2*s^2)) plus a small negative
    #   sigmoid-like tail for x<0. Fit roughly to E1.
    # A bump: peak ~0.036 at x~3 => A*3*exp(-9/(2s^2)) ~ 0.036.
    # Negative tail saturating ~ -0.003 for x<-40.
    # Use: bump term + negative logistic tail.
    x = probe.get("x", [])
    ys = []
    for v in x:
        try:
            v = float(v)
            # positive bump (Gaussian-derivative-like), peak near 3
            bump = 0.036 * (v / 3.0) * math.exp(-(v*v - 9.0) / 18.0) if v > 0 else 0.0
            # negative tail for x<0, saturating near -0.003
            tail = -0.003 / (1.0 + math.exp((v + 20.0) / 8.0))
            # small negative for moderate positive
            small = -0.0005 * math.exp(-((v - 21.0) ** 2) / 2000.0) if v > 10 else 0.0
            ys.append(bump + tail + small)
        except Exception:
            ys.append(None)
    return {"y": ys}

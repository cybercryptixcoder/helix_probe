def predict(probe):
    # Output is a piecewise-linear V with a narrow Gaussian dip at x=0.
    # Left arm (x<=0): y = -1.6815 - 0.00169*x  [E2: -120..-20 linear, slope -0.00169]
    # Right arm (x>0): y = -1.6911 + 0.00142*x  [E2: 20..120 linear, slope 0.00142]
    # Narrow dip at x=0: -0.070*exp(-(x/1.5)^2)  [E2: y(0)=-1.756 vs base ~-1.686]
    # Dip width ~1.5 from E1: at x=2.9 dip only ~0.002 [E1]
    import math
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            base = (-1.6815 - 0.00169 * x) if x <= 0 else (-1.6911 + 0.00142 * x)
            dip = -0.070 * math.exp(-(x / 1.5) ** 2)
            out.append(base + dip)
        except Exception:
            out.append(None)
    return {"y": out}

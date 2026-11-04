def predict(probe):
    # f is smooth and nearly linear in x, decreasing as x increases [E2]
    # Slope ~ (y(128)-y(-128))/(256) = (-1.5099 - -1.4667)/256 ≈ -0.000169 per unit [E2]
    # Intercept at x=0: y(0) = -1.756, a local dip below the linear trend [E2]
    # There is a narrow dip/bump near x=0 (y(0)=-1.756 vs trend ~-1.53) [E2]
    # Elsewhere values follow the line closely: x=10 -> -1.677, x=-10 -> -1.664 [E2]
    # Random probes agree with the line: x=123.6 -> -1.516, x=104.5 -> -1.543 [E3]
    # x=1.2 -> -1.756, x=-6 -> -1.671, x=2.9 -> -1.689: dip is near x≈0, width ~few units [E1,E3]
    import math
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        # linear baseline
        y = -1.53 - 0.000169 * x
        # narrow dip centered near x=0 (Gaussian), depth ~0.22, width ~3
        y -= 0.22 * math.exp(-(x * x) / (2 * 3.0 * 3.0))
        ys.append(y)
    return {"y": ys}

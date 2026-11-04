def predict(probe):
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            out.append(None)
            continue
        # Piecewise linear fit to E1
        # Outside near-zero interval: slope ~ -0.57, anchored at x=-128 -> 76.13
        # Inside interval [-2, 5]: steeper slope ~ -2.0, anchored at x=0 -> -8.83
        if -2.0 <= x <= 5.0:
            y = -8.83 + (-2.0) * x
        elif x < -2.0:
            # slope -0.57 anchored at x=-2 -> -2.56
            y = -2.5588 + (-0.57) * (x - (-2.0))
        else:  # x > 5.0
            # slope -0.57 anchored at x=5 -> -25.42
            y = -25.4152 + (-0.57) * (x - 5.0)
        out.append(y)
    return {"y": out}

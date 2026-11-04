def predict(probe):
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            out.append(None)
            continue
        if x < -2.0:
            # slope ~ -0.57 anchored at x=-2 -> -2.5588
            y = -2.5588 + (-0.57) * (x - (-2.0))
        elif x <= 5.0:
            # steep near-zero segment, slope ~ -3.3 anchored at x=0 -> -8.8302
            y = -8.8302 + (-3.3) * x
        else:
            # x > 5: steeper than far-left; slope ~ -3.05 anchored at x=5 -> -25.4152
            y = -25.4152 + (-3.05) * (x - 5.0)
        out.append(y)
    return {"y": out}

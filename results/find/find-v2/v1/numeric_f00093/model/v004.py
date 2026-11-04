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
            # straight line, slope ~ -0.57, anchored at f(-2) = -2.5588
            y = -2.5588 + (-0.57) * (x - (-2.0))
        elif x <= 5.0:
            # steep near-zero segment, slope ~ -3.3 anchored at x=0 -> -8.8302
            y = -8.8302 + (-3.3) * x
        else:
            # x > 5: slope ~ -3.05 near 5, shallowing toward ~ -1.0 near 30
            if x <= 5.5:
                y = -25.4152 + (-3.05) * (x - 5.0)
            elif x <= 12.0:
                y = -26.9386 + (-2.05) * (x - 5.5)
            else:
                y = -38.0921 + (-0.97) * (x - 12.0)
        out.append(y)
    return {"y": out}

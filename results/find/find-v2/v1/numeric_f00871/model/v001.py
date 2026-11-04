def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                x = float(x)
            except Exception:
                ys.append(None)
                continue
            if x <= -4.0 or x >= 4.0:
                ys.append(0.0)
            else:
                # linear ramp: slope -2.5, intercept 5.2, clamped at 0
                y = 5.2 - 2.5 * x
                if y < 0:
                    y = 0.0
                ys.append(y)
        return {"y": ys}
    except Exception:
        return {"y": []}

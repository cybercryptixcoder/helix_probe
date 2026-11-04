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
            # Zero region outside active interval
            if x <= -2.5 or x >= 4:
                ys.append(0.0)
            else:
                y = 5.2 - 2.5 * x
                # Clamp negative values to -0.0 at and above 2.1
                if x >= 2.1 and y < 0:
                    y = -0.0
                ys.append(y)
        return {"y": ys}
    except Exception:
        return {"y": []}

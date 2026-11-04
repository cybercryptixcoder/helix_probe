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
                y = 5.2 - 2.5 * x
                # Clamp to 0 only above ~2.095 (between 2.09 and 2.1 per E3)
                if x > 2.095 and y < 0:
                    y = 0.0
                ys.append(y)
        return {"y": ys}
    except Exception:
        return {"y": []}

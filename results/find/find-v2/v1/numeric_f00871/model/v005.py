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
            # Zero region: outside the active interval (narrowed per E5)
            if x <= -3.99 or x >= 3.99:
                ys.append(0.0)
            else:
                y = 5.2 - 2.5 * x
                # Clamp to 0 at and above 2.1 (E4)
                if x >= 2.1 and y < 0:
                    y = 0.0
                ys.append(y)
        return {"y": ys}
    except Exception:
        return {"y": []}

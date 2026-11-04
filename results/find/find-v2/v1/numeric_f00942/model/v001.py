def predict(probe):
    try:
        xs = probe["x"]
    except Exception:
        return {}
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        if x > 0:
            y = -405.0 * x + 20.0
        elif x < 0:
            y = -35.5 * x + 5.0
        else:
            y = -5401.17
        ys.append(y)
    return {"y": ys}

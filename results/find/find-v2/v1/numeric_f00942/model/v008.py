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
            y = -405.5 * x - 154.8
        elif x == 0:
            y = -5401.17
        elif x > -1:
            y = -35.72 * x - 17.1
        else:
            y = -35.52 * x - 16.9
        ys.append(y)
    return {"y": ys}

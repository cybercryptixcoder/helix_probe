def predict(probe):
    """Model: piecewise.
    x <= -1: x - 1
    -1 < x <= 0: -1
    0 < x <= 1: 2
    1 < x <= 2: 3
    x > 2: ceil(x) + 1  (fits E1 large values and E4 step pattern)
    """
    import math
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
            elif x <= -1:
                ys.append(x - 1)
            elif x <= 0:
                ys.append(-1)
            elif x <= 1:
                ys.append(2)
            elif x <= 2:
                ys.append(3)
            else:
                ys.append(math.ceil(x) + 1)
        return {"y": ys}
    except Exception:
        return {"y": []}

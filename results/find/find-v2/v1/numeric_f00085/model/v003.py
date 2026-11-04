def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            a = 3.088
            b = -2.5
            c = -22.8021
            plateau = -22.8021
            # Flat region observed at least on [-6, 5.5]; true edges unknown.
            if -6.0 <= x <= 5.5:
                ys.append(plateau)
            else:
                ys.append(a * x * x + b * x + c)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            # Quadratic model fit to E1: y ≈ a*x^2 + b*x + c
            a = 3.088
            b = -2.5
            c = -22.0
            ys.append(a * x * x + b * x + c)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

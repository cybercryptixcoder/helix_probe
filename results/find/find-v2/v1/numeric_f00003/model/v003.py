def predict(probe):
    """Model: flat plateau -20.4469 on [-20, 3.9]; quadratic growth outside, asymmetric."""
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            if x is None:
                out.append(None)
                continue
            x = float(x)
            if -20.0 <= x <= 3.9:
                y = -20.4469
            elif x > 3.9:
                # right side quadratic fit through E3 points x=5..10
                # y+20.4469 = a*x^2 + b*x ; a~63.05, b~-562.5
                a = 63.05
                b = -562.5
                y = a * x * x + b * x - 20.4469
            else:
                # left side: quadratic through (-22,54.04),(-128,24838.95), anchored at plateau
                x1, y1 = -22.0, 54.0378
                x2, y2 = -128.0, 24838.9457
                c = -20.4469
                r1 = y1 - c
                r2 = y2 - c
                det = x1 * x1 * x2 - x2 * x2 * x1
                a = (r1 * x2 - r2 * x1) / det
                b = (x1 * x1 * r2 - x2 * x2 * r1) / det
                y = a * x * x + b * x + c
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

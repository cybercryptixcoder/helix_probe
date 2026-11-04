def predict(probe):
    """Model: flat plateau -20.4469 on [-20, 3]; quadratic growth outside, asymmetric."""
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            if x is None:
                out.append(None)
                continue
            x = float(x)
            if -20.0 <= x <= 3.0:
                y = -20.4469
            elif x > 3.0:
                # right side: quadratic through (5,48.39),(40,5505.53),(128,39006.12)
                a = 2.3796
                b = -3.0
                c = -20.4469
                y = a * x * x + b * x + c
            else:
                # left side: fit through (-22,54.04),(-40,1531.87),(-128,24838.95)
                # solve a*x^2 + b*x + c with c=-20.4469 anchored at plateau
                # use two points to get a,b
                import math
                x1, y1 = -22.0, 54.0378
                x2, y2 = -128.0, 24838.9457
                c = -20.4469
                # a*x1^2 + b*x1 = y1 - c ; a*x2^2 + b*x2 = y2 - c
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

def predict(probe):
    """Model: flat plateau -20.4469 on [-20, 3.75]; quadratic growth outside, asymmetric."""
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            if x is None:
                out.append(None)
                continue
            x = float(x)
            if -20.0 <= x <= 3.75:
                y = -20.4469
            elif x > 3.75:
                a = 63.05
                b = -562.5
                y = a * x * x + b * x - 20.4469
            else:
                # left side: quadratic anchored at plateau edge x=-20.5 (y=-20.4469)
                # through (-30, 548.2541) and (-128, 24838.9457)
                c = -20.4469
                x0 = -20.5
                x1, y1 = -30.0, 548.2541
                x2, y2 = -128.0, 24838.9457
                # y - c = A*(x-x0)^2 + B*(x-x0)
                u1 = x1 - x0
                u2 = x2 - x0
                r1 = y1 - c
                r2 = y2 - c
                det = u1 * u1 * u2 - u2 * u2 * u1
                A = (r1 * u2 - r2 * u1) / det
                B = (u1 * u1 * r2 - u2 * u2 * r1) / det
                u = x - x0
                y = A * u * u + B * u + c
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

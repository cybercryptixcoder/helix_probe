def predict(probe):
    """Model: flat plateau -20.4469 on [-20.1, 3.75]; linear rise on left near edge, then steeper; right rises quadratically."""
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            if x is None:
                out.append(None)
                continue
            x = float(x)
            if -20.1 <= x <= 3.75:
                y = -20.4469
            elif x > 3.75:
                # right side: fit quadratic through (4,-12.9234),(10,650.4807),(128,39006.1248)
                # y = a x^2 + b x + c
                import math
                pts = [(4.0, -12.9234), (10.0, 650.4807), (128.0, 39006.1248)]
                (x1, y1), (x2, y2), (x3, y3) = pts
                # solve for a,b,c
                d = (x1 - x2) * (x1 - x3) * (x2 - x3)
                a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / d
                b = (x3 * x3 * (y1 - y2) + x2 * x2 * (y3 - y1) + x1 * x1 * (y2 - y3)) / d
                c = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / d
                y = a * x * x + b * x + c
            else:
                # left side
                if x >= -21.0:
                    # linear rise from (-20.1, -20.4469) with slope 41.12
                    y = -20.4469 + 41.12 * (x - (-20.1))
                else:
                    # steeper region: interpolate through (-21,12.9172),(-22,54.0378),(-25,204.0128),(-30,548.2541),(-128,24838.9457)
                    pts = [(-128.0, 24838.9457), (-30.0, 548.2541), (-25.0, 204.0128),
                           (-22.0, 54.0378), (-21.0, 12.9172)]
                    # piecewise linear interpolation
                    if x <= pts[0][0]:
                        y = pts[0][1]
                    elif x >= pts[-1][0]:
                        y = pts[-1][1]
                    else:
                        y = None
                        for i in range(len(pts) - 1):
                            xa, ya = pts[i]
                            xb, yb = pts[i + 1]
                            if xa <= x <= xb:
                                t = (x - xa) / (xb - xa)
                                y = ya + t * (yb - ya)
                                break
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

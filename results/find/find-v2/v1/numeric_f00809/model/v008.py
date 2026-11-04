import random

def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        # Deterministic region knots from E9/E10 (x, y)
        knots = [(-128.0, 0.0046), (-120.0, 0.0049), (-110.0, 0.0053),
                 (-100.0, 0.0059), (-95.0, 0.0062), (-90.0, 0.0065),
                 (-85.0, 0.0069), (-80.0, 0.0074)]
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            try:
                xf = float(x)
            except Exception:
                ys.append(None)
                continue
            if -128.0 <= xf <= -80.0:
                # piecewise-linear interpolation over knots
                y = None
                for i in range(len(knots) - 1):
                    x0, y0 = knots[i]
                    x1, y1 = knots[i + 1]
                    if x0 <= xf <= x1:
                        t = (xf - x0) / (x1 - x0)
                        y = y0 + t * (y1 - y0)
                        break
                if y is None:
                    y = 0.0046
                ys.append(round(y, 4))
                continue
            # Stochastic region
            y = random.gauss(0.0, 0.10)
            y = max(-0.30, min(0.35, y))
            ys.append(round(y, 4))
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

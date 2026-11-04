import math

def predict(probe):
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            out.append(None)
            continue
        if x <= 0:
            out.append(None)
        else:
            # Fit a saturating curve through the observed points.
            # Try y = a*ln(x) + b using two anchor points (x=1 -> -7.8, x=128 -> 36.365)
            # then blend with a power-law-ish shape. Keep it simple and monotone.
            try:
                # log model anchored at x=1 and x=128
                a = (36.365 - (-7.8)) / (math.log(128.0) - math.log(1.0))
                b = -7.8
                y_log = a * math.log(x) + b
                # power model y = c * x**p anchored similarly
                # solve p from ratio
                # (y2-b)/(y1-b) = (x2/x1)^p with y1 at x=1
                y1, y2 = -7.8, 36.365
                # shift to positive
                s = 8.0
                p = math.log((y2 + s) / (y1 + s)) / math.log(128.0)
                y_pow = (y1 + s) * (x ** p) - s
                # average the two estimates
                y = 0.5 * (y_log + y_pow)
                out.append(round(y, 4))
            except Exception:
                out.append(None)
    return {"y": out}

import math

def predict(probe):
    """Model: f(x) = ceil(x) for |x| <= 4.35, else 0."""
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                xv = float(x)
            except Exception:
                ys.append(None)
                continue
            if abs(xv) <= 4.35:
                ys.append(float(math.ceil(xv)))
            else:
                ys.append(0.0)
        return {"y": ys}
    except Exception:
        return {"y": []}

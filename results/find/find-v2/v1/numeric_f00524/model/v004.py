import math

def predict(probe):
    """Model: f(x) = ceil(x) for |x| < 4.4, else 0. (ceil(0)=0, integers map to themselves.)"""
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                xv = float(x)
            except Exception:
                ys.append(None)
                continue
            if abs(xv) < 4.4:
                ys.append(float(math.ceil(xv)))
            else:
                ys.append(0.0)
        return {"y": ys}
    except Exception:
        return {"y": []}

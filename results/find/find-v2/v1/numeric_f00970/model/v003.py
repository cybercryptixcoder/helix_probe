import math

def predict(probe):
    """Piecewise model: ~12.5 on [-3,3], small bounded values elsewhere."""
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                x = float(x)
            except Exception:
                ys.append(None)
                continue
            if -3.0 <= x <= 3.0:
                ys.append(12.5)
            else:
                ys.append(0.5 * math.sin(x))
        return {"y": ys}
    except Exception:
        return {"y": []}

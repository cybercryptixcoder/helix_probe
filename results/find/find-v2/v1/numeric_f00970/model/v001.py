import math

def predict(probe):
    """Rough piecewise model: ~13 on [-2,2], small values elsewhere."""
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                x = float(x)
            except Exception:
                ys.append(None)
                continue
            if -2.0 <= x <= 2.0:
                # plateau region, observed ~12.3 to 13.8
                ys.append(13.0)
            else:
                # small bounded term; use a mild oscillation as placeholder
                ys.append(0.5 * math.sin(x))
        return {"y": ys}
    except Exception:
        return {"y": []}

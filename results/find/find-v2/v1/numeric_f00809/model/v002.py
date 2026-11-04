import math

def predict(probe):
    """Best guess: outputs look like small pseudo-random values; model as a
    deterministic hash-like function of x scaled to roughly [-0.25, 0.13]."""
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            # deterministic pseudo-random in [0,1)
            h = math.sin(x * 12.9898 + 78.233) * 43758.5453
            frac = h - math.floor(h)
            # map to roughly observed range [-0.25, 0.13]
            y = -0.25 + frac * 0.38
            ys.append(round(y, 4))
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

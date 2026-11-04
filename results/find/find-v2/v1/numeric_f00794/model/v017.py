import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                x = float(x)
            except Exception:
                ys.append(None)
                continue
            if abs(x) < 1e-9:
                ys.append(475.0)
                continue
            if 0.0 < x <= 0.750:
                ys.append(13.5)
                continue
            if -0.75 <= x < 0.0:
                ys.append(6.8)
                continue
            # base region: pseudo-random noise in [-1, 1], deterministic per x
            h = math.sin(x * 12.9898 + 78.233) * 43758.5453
            frac = h - math.floor(h)
            ys.append(2.0 * frac - 1.0)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

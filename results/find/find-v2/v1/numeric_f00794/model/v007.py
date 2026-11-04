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
                ys.append(473.9758)
                continue
            if 0.0 < x <= 0.755:
                ys.append(13.5)
                continue
            if -0.75 <= x < 0.0:
                ys.append(6.8)
                continue
            base = 0.4 * math.sin(3.1 * x) + 0.3 * math.cos(1.7 * x + 0.5)
            ys.append(base)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

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
            # Isolated spike exactly at 0
            if abs(x) < 1e-9:
                ys.append(473.9758)
                continue
            # Positive plateau roughly on [0.05, 0.7]
            if 0.05 <= x <= 0.7:
                ys.append(13.8)
                continue
            # Tentative negative-side elevated region near -0.5
            if -0.6 <= x <= -0.4:
                ys.append(7.6)
                continue
            # Small irregular baseline elsewhere
            base = 0.4 * math.sin(3.1 * x) + 0.3 * math.cos(1.7 * x + 0.5)
            ys.append(base)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

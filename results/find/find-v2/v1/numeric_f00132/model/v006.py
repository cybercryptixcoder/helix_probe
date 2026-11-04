import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            if x is None:
                out.append(None)
                continue
            y = 4.7093 * x + 3.92
            # narrow S-shaped correction: negative for x<0, positive for x>0,
            # peaking around |x|~0.5 and decaying by |x|~1.5
            y += 1.05 * (x / 0.7) * math.exp(-(x / 0.7) ** 2)
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}

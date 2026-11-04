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
            # smooth odd S-shaped correction: negative for x<0, positive for x>0,
            # peaking around |x|~0.5-0.7 and decaying by |x|~1.5-2
            y += 0.55 * (x / 1.0) * math.exp(-(x / 1.0) ** 2)
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}

import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            if x is None:
                out.append(None)
                continue
            # Global linear trend
            y = 4.7093 * x + 3.92
            # Small smooth correction near zero (S-shaped, odd-ish)
            # Negative side dips slightly below line, positive side rises slightly above
            y += 0.55 * math.tanh(x / 0.9)
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}

import math

def predict(probe):
    """Model: f(x) = floor(x) + sign(x) for x != 0; f(0) = -1 (uncertain)."""
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            try:
                if x is None:
                    out.append(None)
                elif x == 0:
                    out.append(-1.0)
                elif x > 0:
                    out.append(float(math.floor(x)) + 1.0)
                else:
                    out.append(float(math.floor(x)) - 1.0)
            except Exception:
                out.append(None)
        return {"y": out}
    except Exception:
        return {"y": []}

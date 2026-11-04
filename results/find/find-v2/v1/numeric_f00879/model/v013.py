import math

def predict(probe):
    """Stochastic box: return the conditional mean as a smooth trend in x."""
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            try:
                x = float(x)
            except Exception:
                out.append(None)
                continue
            if not math.isfinite(x):
                out.append(None)
                continue
            rise = 2.3 / (1.0 + math.exp(-(x - 0.3) / 0.35))
            left = -1.3 / (1.0 + math.exp((x + 4.0) / 2.0))
            right = -1.0 / (1.0 + math.exp(-(x - 6.0) / 4.0))
            base = rise + left + right
            out.append(base)
        return {"y": out}
    except Exception:
        return {"y": []}

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
            # Gentle sigmoid trend centered near x=-1.5, modest amplitude.
            base = 0.0 + 1.2 * math.tanh((x + 1.5) / 3.0)
            out.append(base)
        return {"y": out}
    except Exception:
        return {"y": []}

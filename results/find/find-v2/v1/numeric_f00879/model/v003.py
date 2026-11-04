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
            # Weak positive trend, saturating for large |x|.
            # Centered near ~1.0 at x=0, rising toward ~2.2 for moderate positive x.
            base = 1.0 + 0.6 * math.tanh(x / 8.0)
            out.append(base)
        return {"y": out}
    except Exception:
        return {"y": []}

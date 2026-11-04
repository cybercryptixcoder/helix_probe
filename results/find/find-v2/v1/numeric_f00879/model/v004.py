import math

def predict(probe):
    """Stochastic box: return the conditional mean as a smooth increasing trend in x."""
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
            # Smooth increasing trend, saturating at large |x|.
            # Centered so mean ~0 near x=-1, ~2.2 near x=1-3, ~0.2 near x=-3.
            base = 1.1 + 1.1 * math.tanh((x + 0.5) / 3.0)
            out.append(base)
        return {"y": out}
    except Exception:
        return {"y": []}

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
            # Smooth trend: rises from ~-1.3 at far left, crosses zero near x=-0.5,
            # reaches ~+2.2 around x=1-2, then plateaus near +1 far right.
            # Use a sigmoid-like rise centered near x=0.2 plus a gentle far-right decay.
            rise = 2.2 / (1.0 + math.exp(-(x - 0.2) / 0.6))
            # Far-left baseline and far-right plateau adjustment
            left = -1.3 / (1.0 + math.exp((x + 4.0) / 2.0))
            right = -1.0 / (1.0 + math.exp(-(x - 6.0) / 4.0))
            base = rise + left + right
            out.append(base)
        return {"y": out}
    except Exception:
        return {"y": []}

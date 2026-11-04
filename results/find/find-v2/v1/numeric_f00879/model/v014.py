import math

def predict(probe):
    """Stochastic box: return the conditional mean as a step function in x."""
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
            if x < 0:
                # left side: ~0 near 0, dropping to ~-1.3 far left
                # smooth transition from -1.3 (far left) to 0 (near 0)
                left = -1.3 / (1.0 + math.exp((x + 4.0) / 2.0))
                val = left
            else:
                # right side: step to ~2 at x=0+, plateau ~2 through ~2.5, decay to ~1 far right
                # plateau value ~2.0, decaying toward ~1 for large x
                plateau = 2.0
                decay = -1.0 / (1.0 + math.exp(-(x - 6.0) / 4.0))
                val = plateau + decay
            out.append(val)
        return {"y": out}
    except Exception:
        return {"y": []}

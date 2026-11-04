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
            # Smooth increasing sigmoid.
            # Floor ~ -1.6 (mean at x=-6), ceiling ~ 2.0 (mean at x=2-3),
            # centered near x ~ -1.5 (zero crossing), moderate width.
            base = 0.2 + 1.8 * math.tanh((x + 1.5) / 2.5)
            out.append(base)
        return {"y": out}
    except Exception:
        return {"y": []}

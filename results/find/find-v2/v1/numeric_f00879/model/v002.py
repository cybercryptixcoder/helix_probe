import math

def predict(probe):
    """Noisy function with a weak linear-ish trend; no clear special interval yet."""
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
            base = 0.02 * x
            noise = 1.5 * math.sin(3.7 * x + 0.3) + 0.8 * math.cos(1.3 * x)
            out.append(base + noise)
        return {"y": out}
    except Exception:
        return {"y": []}

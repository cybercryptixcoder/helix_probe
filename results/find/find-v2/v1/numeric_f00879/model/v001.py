import math
import random

def predict(probe):
    """Best guess: noisy function with a weak linear-ish trend, no clear special interval yet."""
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
            # weak trend: slightly positive for positive x, slightly negative for negative x
            base = 0.02 * x
            # deterministic pseudo-noise derived from x so predictions are reproducible
            noise = 1.5 * math.sin(3.7 * x + 0.3) + 0.8 * math.cos(1.3 * x)
            out.append(base + noise)
        return {"y": out}
    except Exception:
        return {"y": []}

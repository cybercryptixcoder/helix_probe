import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                x = float(x)
            except Exception:
                ys.append(None)
                continue
            # Sharp peak near x=0 (singularity-like), small irregular baseline elsewhere
            peak = 474.0 * math.exp(-(x / 0.35) ** 2)
            # Irregular small baseline: deterministic pseudo-noise via sines
            base = 0.4 * math.sin(3.1 * x) + 0.3 * math.cos(1.7 * x + 0.5)
            ys.append(peak + base)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

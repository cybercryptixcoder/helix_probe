import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            # Smooth oscillatory model fit to E1 observations.
            # Combination of low-frequency sinusoids plus constant.
            v = (
                0.0
                + 0.045 * math.sin(0.049 * x + 0.3)
                + 0.030 * math.sin(0.11 * x - 0.6)
                + 0.020 * math.sin(0.25 * x + 1.2)
                - 0.015 * math.cos(0.02 * x)
            )
            ys.append(v)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

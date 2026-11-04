import random

def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            y = random.gauss(0.0, 0.10)
            # clip to plausible observed range
            y = max(-0.30, min(0.35, y))
            ys.append(round(y, 4))
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

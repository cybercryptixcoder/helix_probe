import random

def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            # Known constant-output inputs (from observations so far)
            if x is not None and abs(x - (-100.0)) < 1e-9:
                ys.append(0.0059)
                continue
            if x is not None and abs(x - (-128.0)) < 1e-9:
                ys.append(0.0046)
                continue
            if x is not None and abs(x - (-127.9999)) < 1e-9:
                ys.append(0.0046)
                continue
            # Otherwise: i.i.d. noise around 0
            y = random.gauss(0.0, 0.10)
            y = max(-0.30, min(0.35, y))
            ys.append(round(y, 4))
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

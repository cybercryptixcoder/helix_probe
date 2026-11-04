import random

def predict(probe):
    """Best guess: f is stochastic; outputs look like noise in roughly
    [-0.24, 0.15]. Return a random value in that range per input."""
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            y = random.uniform(-0.24, 0.15)
            ys.append(round(y, 4))
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

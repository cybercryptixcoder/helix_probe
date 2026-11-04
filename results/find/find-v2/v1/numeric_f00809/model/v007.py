import random

def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            try:
                xf = float(x)
            except Exception:
                ys.append(None)
                continue
            # Far-negative deterministic smooth region (approx [-128, -80])
            if -128.0 <= xf <= -80.0:
                # Linear fit: at -128 -> 0.0046, at -80 -> 0.0074
                # slope = (0.0074 - 0.0046) / (-80 - (-128)) = 0.0028/48
                y = 0.0046 + (xf - (-128.0)) * (0.0028 / 48.0)
                ys.append(round(y, 4))
                continue
            # Otherwise: i.i.d. noise around 0
            y = random.gauss(0.0, 0.10)
            y = max(-0.30, min(0.35, y))
            ys.append(round(y, 4))
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

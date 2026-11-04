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
            # Far-negative deterministic smooth region (approx [-128, -90])
            if -128.0 <= xf <= -90.0:
                # Linear fit through E9: at -128 -> 0.0046, at -90 -> 0.0065
                # slope = (0.0065 - 0.0046) / (-90 - (-128)) = 0.0019/38
                y = 0.0046 + (xf - (-128.0)) * (0.0019 / 38.0)
                ys.append(round(y, 4))
                continue
            # Otherwise: i.i.d. noise around 0
            y = random.gauss(0.0, 0.10)
            y = max(-0.30, min(0.35, y))
            ys.append(round(y, 4))
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

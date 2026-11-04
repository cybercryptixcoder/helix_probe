import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            # Left side: rise to plateau ~0.078 near x=-1, gentle fall toward -128
            left = 0.078 * math.exp(-((x + 1.0) / 40.0) ** 2) if x < 0 else 0.0
            # Central drop: sigmoid-like transition through 0
            # At x=-1: ~0.078; x=0: ~0; x=1: ~-0.095
            # Use a smooth blend
            if x <= -1.0:
                v = 0.078 - 0.0001 * (x + 1.0) ** 2 * 0.0
                # gentle decline far left
                v = 0.078 * math.exp(-((x + 1.0) / 60.0) ** 2) + 0.0001 * (x + 1.0)
            elif x <= 1.0:
                # smooth interpolation from 0.078 at -1 to -0.095 at 1
                t = (x + 1.0) / 2.0
                # ease with cosine
                v = 0.078 + (-0.095 - 0.078) * (0.5 - 0.5 * math.cos(math.pi * t))
            else:
                # right side: rise from -0.095 at 1 toward positive, with oscillation
                v = -0.095 + 0.152 * (1 - math.exp(-(x - 1.0) / 30.0))
                v += 0.02 * math.sin(0.05 * (x - 1.0))
            ys.append(v)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

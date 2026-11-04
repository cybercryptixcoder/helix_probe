import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            if x <= -2.0:
                # Left of plateau: decline from ~0.0784 at -2 toward minimum ~0.0156 at -18,
                # then rise toward ~0.0479 at -128.
                if x >= -18.0:
                    # linear decline: -2 -> 0.0784, -18 -> 0.0156
                    t = (x - (-2.0)) / (-18.0 - (-2.0))  # 0 at -2, 1 at -18
                    v = 0.0784 + (0.0156 - 0.0784) * t
                else:
                    # linear rise: -18 -> 0.0156, -128 -> 0.0479
                    t = (x - (-18.0)) / (-128.0 - (-18.0))  # 0 at -18, 1 at -128
                    v = 0.0156 + (0.0479 - 0.0156) * t
                ys.append(v)
            elif x <= -1.0:
                # plateau region, very slightly decreasing toward -1
                t = (x + 2.0) / 1.0
                v = 0.0784 + (0.0776 - 0.0784) * t
                ys.append(v)
            elif x <= 1.0:
                # smooth cosine transition from 0.0776 at -1 through ~0 at 0 to -0.0951 at 1
                t = (x + 1.0) / 2.0
                v = 0.0776 + (-0.0951 - 0.0776) * (0.5 - 0.5 * math.cos(math.pi * t))
                ys.append(v)
            else:
                # right side: smooth monotone rise from -0.0951 at 1 toward ~0.057 at 128
                # Fit: -0.0951 at 1, -0.0466 at 3, -0.0208 at 12, 0.0003 at 24, 0.0176 at 56, 0.048 at 112
                d = x - 1.0
                v = -0.0951 + 0.075 * (1 - math.exp(-d / 2.5)) + 0.00045 * d
                ys.append(v)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

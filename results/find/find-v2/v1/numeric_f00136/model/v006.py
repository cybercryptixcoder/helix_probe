import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            if x <= -18.0:
                # linear rise: -18 -> 0.0156, -128 -> 0.0479
                t = (x - (-18.0)) / (-128.0 - (-18.0))
                v = 0.0156 + (0.0479 - 0.0156) * t
                ys.append(v)
            elif x <= -14.0:
                # decline from 0.0156 at -18 to min ~0.0142 at -14
                t = (x - (-18.0)) / (-14.0 - (-18.0))
                v = 0.0156 + (0.0142 - 0.0156) * t
                ys.append(v)
            elif x <= -6.0:
                # rise from 0.0142 at -14 to 0.0471 at -6 (smooth, slightly convex)
                t = (x - (-14.0)) / (-6.0 - (-14.0))
                # smoothstep-ish to match E6 curvature
                s = t * t * (3 - 2 * t)
                v = 0.0142 + (0.0471 - 0.0142) * s
                ys.append(v)
            elif x <= -2.0:
                # rise from 0.0471 at -6 to 0.0784 at -2
                t = (x - (-6.0)) / (-2.0 - (-6.0))
                s = t * t * (3 - 2 * t)
                v = 0.0471 + (0.0784 - 0.0471) * s
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
                d = x - 1.0
                v = -0.0951 + 0.075 * (1 - math.exp(-d / 2.5)) + 0.00045 * d
                ys.append(v)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

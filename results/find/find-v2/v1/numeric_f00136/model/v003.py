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
                # Left of plateau: smooth decline from ~0.0784 at -2 toward ~0.048 at -128
                # Fit: at -2 -> 0.0784, -3 -> 0.0706, -4 -> 0.0628, -4.5 -> 0.0589, -8 -> 0.031, -16 -> 0.0149
                # Use a smooth curve: 0.0784 - k*(|x|-2) with mild curvature; approximate with exp decay toward baseline
                d = (-2.0) - x  # distance left of -2
                # linear-ish near plateau, saturating far left
                v = 0.0784 - 0.0078 * d + 0.00004 * d * d
                # clamp toward a floor near 0.045 at very large negative
                floor = 0.045
                if v < floor:
                    v = floor + (v - floor) * 0.0
                    v = floor
                ys.append(v)
            elif x <= -1.0:
                # plateau region, very slightly decreasing toward -1
                # from 0.0784 at -2 to 0.0776 at -1
                t = (x + 2.0) / 1.0  # 0 at -2, 1 at -1
                v = 0.0784 + (0.0776 - 0.0784) * t
                ys.append(v)
            elif x <= 1.0:
                # smooth cosine transition from 0.0776 at -1 through ~0 at 0 to -0.0951 at 1
                t = (x + 1.0) / 2.0
                v = 0.0776 + (-0.0951 - 0.0776) * (0.5 - 0.5 * math.cos(math.pi * t))
                ys.append(v)
            else:
                # right side: rise from -0.0951 at 1 toward positive, with shallow trough near 16
                base = -0.0951 + 0.152 * (1 - math.exp(-(x - 1.0) / 30.0))
                base += 0.02 * math.sin(0.05 * (x - 1.0))
                ys.append(base)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

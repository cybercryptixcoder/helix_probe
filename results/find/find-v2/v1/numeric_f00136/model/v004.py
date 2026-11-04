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
                # Left of plateau: decline from ~0.0784 at -2 toward ~0.048 at -128
                # Points: -2->0.0784, -3->0.0706, -4->0.0628, -4.5->0.0589, -8->0.031, -16->0.0149, -32->0.0197, -64->0.0288, -128->0.0479
                # Non-monotone far left (rises again past -16); approximate with a smooth curve
                d = (-2.0) - x  # distance left of -2
                # near plateau: linear decline ~0.0078 per unit
                v = 0.0784 - 0.0078 * d
                # far left: curve back up toward ~0.048 at -128; blend in a rising term
                if d > 6.0:
                    # blend from linear value at d=6 (~0.0316) toward 0.0479 at d=126
                    t = (d - 6.0) / 120.0
                    t = min(max(t, 0.0), 1.0)
                    base = 0.0784 - 0.0078 * 6.0  # ~0.0316
                    v = base + (0.0479 - base) * (t * t * (3 - 2 * t))
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
                # Points: 1->-0.0951, 2->-0.0595, 3->-0.0466, 5->-0.0405, 12->-0.0208,
                #         24->0.0003, 56->0.0176, 112->0.048, 128->0.0565
                # Use saturating exponential plus linear term
                d = x - 1.0
                v = -0.0951 + 0.055 * (1 - math.exp(-d / 4.0)) + 0.00095 * d
                ys.append(v)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

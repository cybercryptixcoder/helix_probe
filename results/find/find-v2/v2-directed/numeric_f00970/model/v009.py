import random

def predict(probe):
    # Inside |x| <= 3.05: noisy ~12 [E11,E12,E17,E23 repeated-call spread]
    # Outside |x| > 3.05: noisy ~0 [E1,E4,E13,E16,E18,E19,E20]
    # Boundary is 3.05 inclusive inside [E14,E15,E18,E20]
    # Noise appears roughly Gaussian, std ~1 inside, ~1 outside [E11,E12,E16]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        try:
            xv = float(x)
        except Exception:
            ys.append(None)
            continue
        if -3.05 <= xv <= 3.05:
            ys.append(round(random.gauss(12.0, 1.0), 4))
        else:
            ys.append(round(random.gauss(0.0, 1.0), 4))
    return {"y": ys}

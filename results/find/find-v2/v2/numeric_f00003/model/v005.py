import math

def predict(probe):
    # A: x < -83: linear -319.86x-16103.1 [E6 -90, E7 -124.4]
    # B: -83 <= x < -20.3: quadratic 2.0487x^2+44.64x+41.26 [E1,E3,E6]
    # C: -20.3 <= x <= 4.0: flat floor -20.4469 [E1,E2,E6,E10]
    # D: 4.0 < x <= 19: linear 126.1155x-610.674 [E2,E8,E10]
    # E: 19 < x <= 65.5: quadratic 2.3667x^2+36.5x+235.6 [E4,E8]
    # F: 65.5 < x <= 77.5: quadratic 2.6174x^2-2.55x+1717.7 [E1,E4]
    # G: x > 77.5: linear 430.95x-16155.6 [E3,E5,E7,E9]
    x = probe.get("x", [])
    ys = []
    FLOOR = -20.4469
    for v in x:
        if v is None:
            ys.append(None); continue
        try:
            v = float(v)
        except Exception:
            ys.append(None); continue
        if v < -83.0:
            y = -319.86*v - 16103.1
        elif v < -20.3:
            y = 2.0487*v*v + 44.64*v + 41.26
        elif v <= 4.0:
            y = FLOOR
        elif v <= 19.0:
            y = 126.1155*v - 610.674
        elif v <= 65.5:
            y = 2.3667*v*v + 36.5*v + 235.6
        elif v <= 77.5:
            y = 2.6174*v*v - 2.55*v + 1717.7
        else:
            y = 430.95*v - 16155.6
        ys.append(y)
    return {"y": ys}

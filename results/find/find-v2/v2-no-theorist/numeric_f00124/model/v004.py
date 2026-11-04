import math

def predict(probe):
    # Beliefs:
    # - For x >= 0.5 the function is a pure quadratic ~1.277*x^2 [E1,E2,E3,E5,E7,E12,E13,E14,E15].
    # - For x <= -1.0 the function is a pure quadratic ~0.42*x^2 [E1,E2,E5,E7,E9,E12,E14,E15].
    # - For x in [-0.6, 0.5] the function is exactly linear slope 110: y=106.0528+110x [E6,E8,E10].
    # - For x in [-1.0, -0.6] there is a smooth bend connecting the two; the model
    #   below uses a quadratic fitted to E16 points (slope ramps from ~0 at -1 to ~110 at -0.6) [E16].
    x = probe.get("x", [])
    out = []
    for v in x:
        try:
            v = float(v)
        except Exception:
            out.append(None)
            continue
        if -0.6 <= v <= 0.5:
            y = 106.0528 + 110.0 * v
        elif -1.0 <= v < -0.6:
            a, b, c = _quad(-1.0, 6.8494, -0.8, 18.223, -0.6, 40.0528)
            y = a * v * v + b * v + c
        elif v > 0.5:
            a, b, c = _quad(2.9, 429.1934, 21.3, 2479.4652, 88.2, 9933.9859)
            y = a * v * v + b * v + c
        else:
            a, b, c = _quad(-6.0, 130.985, -20.3, 503.8102, -61.7, 1583.1784)
            y = a * v * v + b * v + c
        out.append(y)
    return {"y": out}


def _quad(x1, y1, x2, y2, x3, y3):
    d = (x1 - x2) * (x1 - x3) * (x2 - x3)
    if d == 0:
        return 0.0, 0.0, 0.0
    a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / d
    b = (x3 * x3 * (y1 - y2) + x2 * x2 * (y3 - y1) + x1 * x1 * (y2 - y3)) / d
    c = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / d
    return a, b, c

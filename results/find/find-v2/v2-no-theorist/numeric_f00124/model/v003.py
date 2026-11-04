import math

def predict(probe):
    # Beliefs:
    # - For |x| >= ~2 the function is piecewise quadratic: positive side
    #   ~1.277*x^2 (+ tiny linear), negative side ~0.42*x^2 [E1,E2,E3,E5,E7].
    # - On the negative side, x in [-2,-1] follows the negative quadratic
    #   (continuous at x=-1 with y~6.85) [E6,E8].
    # - Central region x in [-1, 0.5] is NOT one straight line [E10]:
    #   * x in [-0.6, 0.5] is exactly linear slope 110: y=106.0528+110x
    #     (106.05 at 0, 161.77 at 0.5, 40.05 at -0.6) [E6,E8,E10].
    #   * x in [-1, -0.6] is a smooth bend (slope ramps ~43 -> ~110)
    #     approximated by a quadratic through (-1,6.8494),(-0.75,22.8773),
    #     (-0.6,40.0528) [E10] (?).
    # - The positive quadratic meets the line continuously at x=0.5 [E6,E8].
    x = probe.get("x", [])
    out = []
    for v in x:
        try:
            v = float(v)
        except Exception:
            out.append(None)
            continue
        if -0.6 <= v <= 0.5:
            # central linear region
            y = 106.0528 + 110.0 * v
        elif -1.0 <= v < -0.6:
            # left transition bend
            a, b, c = _quad(-1.0, 6.8494, -0.75, 22.8773, -0.6, 40.0528)
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

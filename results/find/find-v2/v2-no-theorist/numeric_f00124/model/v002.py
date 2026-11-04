import math

def predict(probe):
    # Beliefs:
    # - For |x| >= ~2 the function is piecewise quadratic: positive side
    #   ~1.277*x^2 (+ tiny linear), negative side ~0.42*x^2 [E1,E2,E3,E5,E7].
    # - There is a special small-|x| region. On the negative side, from
    #   x=-2 down to x=-1 the curve follows the negative quadratic, but
    #   between x=-1 and x=0 it is LINEAR with slope ~ -110 per unit x
    #   (y goes 6.85 at -1 to 106.05 at 0) [E6,E8].
    # - On the positive side, x in [0,0.5] is also linear with the SAME
    #   slope ~110 (106.05 at 0 -> 161.77 at 0.5) [E6,E8].
    # - So near zero the function is a straight line y = 106.05 + 110*x
    #   for x in [-1, 0.5]; outside that it's the piecewise quadratic.
    # - The two quadratics meet the line continuously at x=-1 and x=0.5
    #   (small jumps are within noise) [E6,E8].
    x = probe.get("x", [])
    out = []
    for v in x:
        try:
            v = float(v)
        except Exception:
            out.append(None)
            continue
        if -1.0 <= v <= 0.5:
            # central linear region
            y = 106.0528 + 110.0 * v
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

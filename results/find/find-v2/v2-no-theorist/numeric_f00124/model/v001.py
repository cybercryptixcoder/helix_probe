import math

def predict(probe):
    # Model: f(x) is roughly quadratic-ish in x, but with a sign-dependent
    # structure. Observed y grows with |x| and is larger for positive x.
    # E1 data:
    #   x=88.2 -> 9933.99 ; x=66.0 -> 7460.29 ; x=72.7 -> 8206.85
    #   x=21.3 -> 2479.47 ; x=2.9 -> 429.19 ; x=-6.0 -> 130.99
    #   x=-20.3 -> 503.81 ; x=-24.3 -> 608.10 ; x=-50.4 -> 1288.57
    #   x=-61.7 -> 1583.18
    # Positive side looks like ~ a*x^2 + b*x (roughly 1.28*x^2 for large x).
    # Negative side is much smaller in magnitude: ~0.42*x^2.
    # Fit a piecewise quadratic: y = a*x^2 + b*x + c, different a for x>=0 vs x<0.
    # From E1: positive: 88.2^2=7779.24 -> 9933.99 ; 66^2=4356 -> 7460.29
    #   Solve a*7779.24 + b*88.2 = 9933.99 ; a*4356 + b*66 = 7460.29
    #   a ≈ 1.277, b ≈ 0.0 (roughly). Check 72.7: 1.277*5285.29=6749 vs 8206 -> b>0.
    #   Use two points: a=(9933.99/88.2 - 7460.29/66)/(88.2-66)
    #     9933.99/88.2=112.63 ; 7460.29/66=113.03 -> slope negative small.
    #   Actually y/x: 112.63, 113.03, 112.89, 116.41, 148.0, ... not linear.
    # Try y = a*x^2 + b*x + c with c small.
    # Positive: use (2.9,429.19),(21.3,2479.47),(88.2,9933.99)
    # Negative: use (-6,130.99),(-20.3,503.81),(-61.7,1583.18)
    # I'll fit each side with quadratic through 3 points.
    x = probe.get("x", [])
    out = []
    for v in x:
        try:
            v = float(v)
        except Exception:
            out.append(None)
            continue
        if v >= 0:
            # positive-side quadratic fit from E1 points
            # points: (2.9,429.1934),(21.3,2479.4652),(88.2,9933.9859)
            a, b, c = _quad(2.9, 429.1934, 21.3, 2479.4652, 88.2, 9933.9859)
        else:
            # negative-side quadratic fit: (-6,130.985),(-20.3,503.8102),(-61.7,1583.1784)
            a, b, c = _quad(-6.0, 130.985, -20.3, 503.8102, -61.7, 1583.1784)
        out.append(a * v * v + b * v + c)
    return {"y": out}


def _quad(x1, y1, x2, y2, x3, y3):
    # Solve a*x^2+b*x+c through three points.
    d = (x1 - x2) * (x1 - x3) * (x2 - x3)
    if d == 0:
        return 0.0, 0.0, 0.0
    a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / d
    b = (x3 * x3 * (y1 - y2) + x2 * x2 * (y3 - y1) + x1 * x1 * (y2 - y3)) / d
    c = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / d
    return a, b, c

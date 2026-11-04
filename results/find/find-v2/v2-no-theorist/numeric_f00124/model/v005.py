import math

def predict(probe):
    # Beliefs:
    # - For x >= 0.5: pure quadratic ~1.277*x^2 [E1,E2,E3,E5,E7,E12,E13,E14,E15,E21,E23].
    # - For x <= -1.05: pure quadratic ~0.42*x^2 [E1,E2,E5,E7,E9,E12,E14,E15,E21,E23].
    # - For x in [-0.6, 0.5]: exactly linear, slope 110: y=106.0528+110x [E6,E8,E10,E20,E22].
    # - For x in [-1.05, -0.6]: smooth bend. The bend is NOT a single quadratic; it is
    #   smooth and joins the linear segment at -0.6 (y=40.0528) and the left quadratic
    #   near -1.05 (y~6.4189). Fit a cubic through the dense E24/E16/E18 samples. [E16,E18,E24]
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
        elif -1.05 <= v < -0.6:
            y = _bend(v)
        elif v > 0.5:
            a, b, c = _quad(2.9, 429.1934, 21.3, 2479.4652, 88.2, 9933.9859)
            y = a * v * v + b * v + c
        else:
            a, b, c = _quad(-6.0, 130.985, -20.3, 503.8102, -61.7, 1583.1784)
            y = a * v * v + b * v + c
        out.append(y)
    return {"y": out}


def _bend(v):
    # Cubic fitted to the observed bend samples (E16/E18/E24).
    # Anchor points: (-1.05,6.4189), (-1.0,6.8494), (-0.9,10.6298), (-0.8,18.223), (-0.6,40.0528)
    # Use a smooth cubic through (-1.05,6.4189),(-0.9,10.6298),(-0.75,~22.9),(-0.6,40.0528)
    a, b, c, d = _cubic(-1.05, 6.4189, -0.9, 10.6298, -0.75, 22.9, -0.6, 40.0528)
    return a * v * v * v + b * v * v + c * v + d


def _cubic(x0, y0, x1, y1, x2, y2, x3, y3):
    # Solve for a,b,c,d in a*x^3+b*x^2+c*x+d through 4 points (Gaussian elimination).
    A = [[x0**3, x0**2, x0, 1.0, y0],
         [x1**3, x1**2, x1, 1.0, y1],
         [x2**3, x2**2, x2, 1.0, y2],
         [x3**3, x3**2, x3, 1.0, y3]]
    n = 4
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[p] = A[p], A[i]
        if abs(A[i][i]) < 1e-12:
            return 0.0, 0.0, 0.0, 0.0
        for r in range(n):
            if r != i:
                f = A[r][i] / A[i][i]
                for k in range(i, n + 1):
                    A[r][k] -= f * A[i][k]
    return tuple(A[i][n] / A[i][i] for i in range(n))


def _quad(x1, y1, x2, y2, x3, y3):
    d = (x1 - x2) * (x1 - x3) * (x2 - x3)
    if d == 0:
        return 0.0, 0.0, 0.0
    a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / d
    b = (x3 * x3 * (y1 - y2) + x2 * x2 * (y3 - y1) + x1 * x1 * (y2 - y3)) / d
    c = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / d
    return a, b, c

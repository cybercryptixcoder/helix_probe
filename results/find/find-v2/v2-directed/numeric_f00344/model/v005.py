import math

def predict(probe):
    # Beliefs (revised after E18):
    # - Positive branch x>=1 is f(x) = -A * b^x * x^p with p>0 (super-exponential
    #   growth in the sense that ratio drifts up with x). E18 gives clean integers:
    #   f(1)=-41.7, f(2)=-79.6, f(3)=-211.7, f(5)=-1147.3, f(7)=-3914.1, f(9)=-10038.5,
    #   f(11)=-21507.7, f(13)=-40769.7, f(17)=-114768.1, f(21)=-260833.7, f(25)=-515139.3,
    #   f(33)=-1530025.7, f(49)=-7268662.5, f(65)=-22240963.3, f(97)=-108964880.1,
    #   f(100)=-122991196.8, f(110)=-179674322.8, f(120)=-254003268.8,
    #   f(127)=-318304442.1, f(128)=-328399499.2.
    #   Ratio f(x+1)/f(x) at x=1: 1.909; x=2: 2.659; x=4: 2.173; x=6: 1.765;
    #   x=8: 1.558; x=10: 1.491; x=12: 1.359; x=16: 1.283; x=20: 1.209; x=24: 1.176;
    #   x=32: 1.129; x=48: 1.090; x=64: 1.090; x=96: 1.129; x=99: 1.090; x=109: 1.090;
    #   x=119: 1.090; x=126: 1.090; x=127: 1.032.
    #   Ratio appears to approach ~1.09 at large x (consistent with b~1.09).
    #   Fit f(x) = -A * b^x * x^p via log-linear regression on E18 points.
    # - Negative side x<=-3: clean exponential -A*c^(-x) [E10].
    # - Hump region -3<x<=-1: f(-3)=-15, rises to max ~+0.0743 at x=-2.1,
    #   back to f(-1)=-7.4 [E11,E10].
    # - Negative plateau -1<x<0: f(-1)=-7.4 to f(0-)=-11.692 [E9,E5].
    # - Positive plateau 0<x<1: f(0+)=-36.8 to f(1)=-41.7 [E5,E3,E4].
    # - f(0)=472.73 spike [E1].

    pos_data = [
        (1.0, 41.7), (2.0, 79.6), (3.0, 211.7), (5.0, 1147.3),
        (7.0, 3914.1), (9.0, 10038.5), (11.0, 21507.7), (13.0, 40769.7),
        (17.0, 114768.1), (21.0, 260833.7), (25.0, 515139.3),
        (33.0, 1530025.7), (49.0, 7268662.5), (65.0, 22240963.3),
        (97.0, 108964880.1), (100.0, 122991196.8), (110.0, 179674322.8),
        (120.0, 254003268.8), (127.0, 318304442.1), (128.0, 328399499.2),
    ]
    n = len(pos_data)
    S = [[0.0]*3 for _ in range(3)]
    T = [0.0]*3
    for x, y in pos_data:
        feat = [1.0, x, math.log(x)]
        ly = math.log(y)
        for i in range(3):
            T[i] += feat[i]*ly
            for j in range(3):
                S[i][j] += feat[i]*feat[j]
    def solve3(M, v):
        A = [row[:] + [v[i]] for i, row in enumerate(M)]
        for col in range(3):
            piv = max(range(col,3), key=lambda r: abs(A[r][col]))
            A[col], A[piv] = A[piv], A[col]
            if abs(A[col][col]) < 1e-15:
                return [0.0,0.0,0.0]
            for r in range(3):
                if r != col:
                    f = A[r][col]/A[col][col]
                    for c in range(col,4):
                        A[r][c] -= f*A[col][c]
        return [A[i][3]/A[i][i] for i in range(3)]
    coef = solve3(S, T)
    logA, logb, p_pos = coef
    A_pos = math.exp(logA)
    b_pos = math.exp(logb)

    c_neg = (47610123.7 / 15.0) ** (1.0 / 77.0)
    A_neg = 15.0 / (c_neg ** 3.0)

    def pos_exp(x):
        return -A_pos * (b_pos ** x) * (x ** p_pos)

    def neg_exp(x):
        return -A_neg * (c_neg ** (-x))

    def lagrange(x, pts):
        total = 0.0
        for i, (xi, yi) in enumerate(pts):
            term = yi
            for j, (xj, _) in enumerate(pts):
                if i != j:
                    term *= (x - xj) / (xi - xj)
            total += term
        return total

    def f(x):
        if x == 0:
            return 472.73
        if x >= 1:
            return pos_exp(x)
        if x <= -3:
            return neg_exp(x)
        if -3 < x <= -1:
            return lagrange(x, [(-3.0, -15.0), (-2.1, 0.0743), (-1.0, -7.4)])
        if -1 < x < 0:
            return lagrange(x, [(-1.0, -7.4), (-0.5, -10.375), (0.0, -11.692)])
        return lagrange(x, [(0.0, -36.8), (0.5, -37.825), (1.0, -41.7)])

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(f(float(x)))
        except Exception:
            ys.append(None)
    return {"y": ys}

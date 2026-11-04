import math

def predict(probe):
    # Beliefs:
    # - Positive branch x>=1: f(x) = -A * b^x * x^p. E19 shows f(1)=-41.7, f(2)=-79.6,
    #   f(3)=-211.7, f(4)=-528, f(5)=-1147.3, f(6)=-2217.2, f(7)=-3914.1, f(8)=-6443.2.
    #   Ratios: f(2)/f(1)=1.909, f(3)/f(2)=2.659, f(4)/f(3)=2.494, f(5)/f(4)=2.173,
    #   f(6)/f(5)=1.932, f(7)/f(6)=1.765, f(8)/f(7)=1.646. Ratio drifts down toward ~1.09
    #   at large x [E18]. So f = -A*b^x*x^p with b~1.09 and p>0.
    # - Half-integer points E19: f(1.25)=-46.18, f(1.5)=-53.375, f(1.75)=-64.18,
    #   f(2.25)=-100.77, f(2.5)=-128.925, f(2.75)=-165.41, f(3.25)=-269.36,
    #   f(3.5)=-340.075, f(3.75)=-425.65, f(4.5)=-791.225, f(5.5)=-1615.575,
    #   f(6.5)=-2975.125. These are smooth continuations of the integer values.
    # - Negative side x<=-3: clean exponential -A*c^(-x) [E10].
    # - Hump region -3<x<=-1: f(-3)=-15, max ~+0.0743 at x=-2.1, f(-1)=-7.4 [E11,E10].
    # - Negative plateau -1<x<0: f(-1)=-7.4 to f(0-)=-11.692 [E9,E5].
    # - Positive plateau 0<x<1: f(0+)=-36.8 to f(1)=-41.7 [E5,E3,E4].
    # - f(0)=472.73 spike [E1].

    pos_data = [
        (1.0, 41.7), (2.0, 79.6), (3.0, 211.7), (4.0, 528.0), (5.0, 1147.3),
        (6.0, 2217.2), (7.0, 3914.1), (8.0, 6443.2), (9.0, 10038.5),
        (10.0, 14962.8), (11.0, 21507.7), (12.0, 29993.6), (13.0, 40769.7),
        (14.0, 54214.0), (15.0, 70733.3), (16.0, 90763.2), (17.0, 114768.1),
        (18.0, 143241.2), (20.0, 215708.8), (21.0, 260833.7), (24.0, 439160.0),
        (25.0, 515139.3), (30.0, 1052274.8), (32.0, 1355761.6), (33.0, 1530025.7),
        (40.0, 3262660.8), (48.0, 6699915.2), (49.0, 7268662.5), (50.0, 7872866.8),
        (55.0, 11477277.3), (60.0, 16196892.8), (64.0, 20915544.0),
        (65.0, 22240963.3), (70.0, 29836738.8), (80.0, 50682404.8),
        (90.0, 80911890.8), (96.0, 108964880.1), (97.0, 108964880.1),
        (100.0, 122991196.8), (110.0, 179674322.8), (120.0, 254003268.8),
        (127.0, 318304442.1), (128.0, 328399499.2),
    ]
    # Fit log|f| = logA + x*logb + p*log(x)
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

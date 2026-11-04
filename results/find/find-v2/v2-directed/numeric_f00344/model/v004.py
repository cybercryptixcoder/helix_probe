import math

def predict(probe):
    # Beliefs (revised after E13-E17):
    # - Positive branch x>=1 is NOT a pure exponential. The ratio drifts:
    #   near x=1-3 growth is ~1.9x per unit, near x=60-100 growth is ~2.4x per unit.
    #   Check E15: f(2)/f(1)=1.909, f(3)/f(2)=2.659, f(4)/f(3)=2.494, f(5)/f(4)=2.173,
    #   f(6)/f(5)=1.933, f(7)/f(6)=1.765, f(8)/f(7)=1.646, f(9)/f(8)=1.558,
    #   f(10)/f(9)=1.491, f(11)/f(10)=1.437, f(12)/f(11)=1.394, f(13)/f(12)=1.359,
    #   f(14)/f(13)=1.330, f(15)/f(14)=1.305, f(16)/f(15)=1.283, f(18)/f(16)=1.578,
    #   f(24)/f(18)=3.066, f(32)/f(24)=3.087, f(64)/f(32)=15.43.
    #   This is consistent with f(x) = -A * x^p * b^x form? Let's test: log|f| vs log x.
    #   Actually ratio f(x+1)/f(x) = b * ((x+1)/x)^p. As x->inf ratio->b.
    #   From large x: f(64)/f(32)=15.43 => per unit 15.43^(1/32)=1.0900... hmm.
    #   Let's fit f(x) = -A * b^x * x^p using data.
    #   log|f| = log A + x log b + p log x.
    #   Use E15 points: (1,-41.7),(2,-79.6),(4,-528),(8,-6443.2),(16,-90763.2),(32,-1355761.6),(64,-20915544)
    #   Let me solve numerically in code instead.
    # - Negative side x<=-3: clean exponential -A*c^(-x) [E10].
    #   From f(-3)=-15, f(-80)=-47610123.7: c=(47610123.7/15)^(1/77).
    #   Check f(-4)=-106.1, f(-8)=-3320.5, f(-16)=-66110.9, f(-64)=-19342450.1.
    # - Hump region -3<x<=-1: f(-3)=-15, rises to max ~+0.0743 at x=-2.1,
    #   back to f(-1)=-7.4 [E11,E10].
    # - Negative plateau -1<x<0: f(-1)=-7.4 to f(0-)=-11.692 [E9,E5].
    # - Positive plateau 0<x<1: f(0+)=-36.8 to f(1)=-41.7 [E5,E3,E4].
    # - f(0)=472.73 spike [E1].

    # Fit positive branch: f(x) = -A * b^x * x^p for x>=1
    # Use log-linear regression on log|f| = log A + x*log b + p*log x
    # Data points from E15 (x, |f|):
    pos_data = [
        (1.0, 41.7), (2.0, 79.6), (3.0, 211.7), (4.0, 528.0),
        (5.0, 1147.3), (6.0, 2217.2), (7.0, 3914.1), (8.0, 6443.2),
        (9.0, 10038.5), (10.0, 14962.8), (11.0, 21507.7), (12.0, 29993.6),
        (13.0, 40769.7), (14.0, 54214.0), (15.0, 70733.3), (16.0, 90763.2),
        (18.0, 143241.2), (24.0, 439160.0), (32.0, 1355761.6), (64.0, 20915544.0),
    ]
    # Solve least squares for [logA, logb, p]
    # Build normal equations
    n = len(pos_data)
    # features: [1, x, log(x)]
    import math as _m
    S = [[0.0]*3 for _ in range(3)]
    T = [0.0]*3
    for x, y in pos_data:
        feat = [1.0, x, _m.log(x)]
        ly = _m.log(y)
        for i in range(3):
            T[i] += feat[i]*ly
            for j in range(3):
                S[i][j] += feat[i]*feat[j]
    # Solve 3x3
    def solve3(M, v):
        # Gaussian elimination
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
    A_pos = _m.exp(logA)
    b_pos = _m.exp(logb)

    # Negative exponential (x<=-3)
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

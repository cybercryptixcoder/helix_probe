def predict(probe):
    # f is piecewise: flat plateau in the middle, curved branches outside.
    # Plateau: f = -20.4469 for -20.15 <= x <= 3.95 [E6,E8,E14]
    # Left edge: plateau extends to x=-20.15 inclusive; below that a smooth
    #   rise begins [E6,E8,E14]. At x=-20.2 y=-19.49, x=-20.3 y=-15.87,
    #   x=-20.5 y=-7.64, x=-21.5 y=33.5, x=-22.5 y=74.6 [E6,E8].
    # Left branch: cubic fits well across the far range [E2,E3,E9].
    # Right edge: plateau to x=3.95 inclusive; rise begins above [E6,E8].
    #   At x=4.0 y=-12.92, 4.05 y=-11.11, 4.1 y=-9.30, 4.3 y=-0.94 [E8].
    # Right branch near edge (4-40): quadratic-ish, convex [E12].
    # Right branch far (>40): smooth cubic, nearly linear at large x [E4,E10].

    def poly_fit(xs, ys, deg):
        n = len(xs)
        m = deg + 1
        A = [[0.0]*m for _ in range(m)]
        B = [0.0]*m
        for x, y in zip(xs, ys):
            pw = [x**k for k in range(2*deg+1)]
            for i in range(m):
                B[i] += y * pw[i]
                for j in range(m):
                    A[i][j] += pw[i+j]
        M = [row[:] + [b] for row, b in zip(A, B)]
        for i in range(m):
            piv = max(range(i, m), key=lambda r: abs(M[r][i]))
            M[i], M[piv] = M[piv], M[i]
            if abs(M[i][i]) < 1e-12:
                return [0.0]*(deg) + [sum(ys)/n]
            for r in range(i+1, m):
                f = M[r][i]/M[i][i]
                for c in range(i, m+1):
                    M[r][c] -= f*M[i][c]
        sol = [0.0]*m
        for i in range(m-1, -1, -1):
            s = M[i][m] - sum(M[i][j]*sol[j] for j in range(i+1, m))
            sol[i] = s/M[i][i]
        return sol

    def evalp(coef, x):
        r = 0.0
        for c in reversed(coef):
            r = r*x + c
        return r

    # Left branch: near-edge points plus far points, cubic.
    left_x = [-22.5,-21.5,-20.8,-20.5,-20.3,-20.2,
              -120,-100,-80,-63.9,-61.7,-60,-55.8,-50.4,-40,-30,-24.3]
    left_y = [74.5981,33.4775,4.6931,-7.643,-15.8672,-19.4911,
              22280.0824,15882.924,9582.0843,5554.3344,5086.1272,4736.4186,
              3927.9297,2995.4039,1531.8654,548.2541,166.2134]
    lcoef = poly_fit(left_x, left_y, 3)

    # Right branch split: near-edge (quadratic) and far (cubic).
    near_x = [4.0,4.05,4.1,4.3,4.6,5.0,5.5,6.0,6.5,7.0,7.5,8.5,9.5,11,12.5,14,16,18]
    near_y = [-12.9234,-11.114,-9.3046,-0.9369,20.2023,48.3879,95.9038,146.0188,
              209.0765,272.1343,335.192,461.3075,587.423,776.5962,965.7695,
              1154.9427,1407.1737,1659.4047]
    ncoef = poly_fit(near_x, near_y, 2)

    far_x = [22,24,26,28,32,34,36,38,40,60,65.5,66.0,72.7,79.4,80,88.2,
             100,103.0,104.5,104.9,110,120,128]
    far_y = [2187.6092,2460.9815,2753.1594,3102.7698,3833.4949,4224.9124,
             4632.1784,5057.8282,5505.5302,10959.9624,12779.9647,12950.8364,
             15366.0691,18061.8252,18320.3968,21854.2087,26939.4501,
             28232.3081,28878.7371,29051.1182,31248.9768,35558.5035,39006.1248]
    fcoef = poly_fit(far_x, far_y, 3)

    FLAT = -20.4469
    LEFT_B = -20.15   # plateau includes x=-20.15 [E14]
    RIGHT_B = 3.95    # plateau includes x=3.95 [E6,E8]
    NEAR_FAR = 20.0

    out = []
    for x in probe.get("x", []):
        if x < LEFT_B:
            y = evalp(lcoef, x)
        elif x > RIGHT_B:
            if x <= NEAR_FAR:
                y = evalp(ncoef, x)
            else:
                y = evalp(fcoef, x)
        else:
            y = FLAT
        out.append(y)
    return {"y": out}

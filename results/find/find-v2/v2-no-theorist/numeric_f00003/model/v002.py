def predict(probe):
    # f is piecewise: flat plateau around 0, quadratic-ish on each side.
    # Left branch (x <= ~-20.2): increasing, convex. [E1,E2]
    # Flat region: f = -20.4469 for -20.2 < x < ~4. [E1,E2]
    # Right branch (x >= ~4): increasing, convex. [E1,E2,E3]
    # E3 shows right branch is NOT a single quadratic: at large x the model
    # over-predicted (e.g. x=123.6: 37110 vs 39767), so curvature decreases
    # at large x -> cubic-like (negative x^3 term) fits better. [E3]
    # Left branch also slightly off in E3 (x=-55.8: 3928 vs 4125; x=-63.9:
    # 5554 vs 5698), model over-predicted -> left curvature also decreases
    # at large |x|, cubic-like. [E3]

    def poly_fit(xs, ys, deg):
        n = len(xs)
        # normal equations for polynomial of given degree
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

    left_x = [-120,-100,-80,-63.9,-61.7,-60,-55.8,-50.4,-40,-30,-24.3,-20.3]
    left_y = [22280.0824,15882.924,9582.0843,5554.3344,5086.1272,4736.4186,
              3927.9297,2995.4039,1531.8654,548.2541,166.2134,-15.8672]
    lcoef = poly_fit(left_x, left_y, 3)

    right_x = [5,10,20,21.3,30,30.3,40,60,65.5,66.0,72.7,79.4,80,88.2,
               100,103.0,104.5,104.9,123.6]
    right_y = [48.3879,650.4807,1914.2369,2091.9289,3458.112,3514.4195,
               5505.5302,10959.9624,12779.9647,12950.8364,15366.0691,
               18061.8252,18320.3968,21854.2087,26939.4501,28232.3081,
               28878.7371,29051.1182,37109.9331]
    rcoef = poly_fit(right_x, right_y, 3)

    FLAT = -20.4469
    LEFT_B = -20.15
    RIGHT_B = 3.95

    out = []
    for x in probe.get("x", []):
        if x <= LEFT_B:
            y = evalp(lcoef, x)
        elif x >= RIGHT_B:
            y = evalp(rcoef, x)
        else:
            y = FLAT
        out.append(y)
    return {"y": out}

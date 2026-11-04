def predict(probe):
    # f looks like a cubic polynomial in x over ordinary inputs [E1, E2]
    # E2 small-x values fit y ≈ a*x^3 + b*x^2 + c*x + d
    # Let's estimate coefficients from E2.
    # Using points: x=0 -> 2.789 (d)
    # x=1 -> 1.3305, x=-1 -> 3.8615 => c ≈ (1.3305-3.8615)/2 = -1.2655
    # x=2 -> -23.532, x=-2 -> 31.2373 => 8a+4b = (-23.532+31.2373)/2 - d = 3.85265 - 2.789 = 1.06365... 
    # Actually let's solve properly with least squares mentally is hard; use numpy-free approach.
    # Fit cubic via normal equations using all E2 points.
    xs = [-10,-8,-6,-4,-2,-1,0,1,2,4,6,8,10]
    ys = [3862.6931,1971.3195,824.5018,241.0725,31.2373,3.8615,2.789,1.3305,-23.532,-242.55,-835.361,-1992.1386,-3897.0294]
    # Build normal equations for [x^3, x^2, x, 1]
    import math
    n = len(xs)
    # sums
    S = [0.0]*7  # S[k] = sum x^k, k=0..6
    for x in xs:
        p = 1.0
        for k in range(7):
            S[k] += p
            p *= x
    T = [0.0]*4  # T[j] = sum y * x^j
    for x,y in zip(xs,ys):
        p = 1.0
        for j in range(4):
            T[j] += y*p
            p *= x
    # Matrix M[i][j] = S[i+j] for i,j in 0..3, with basis order x^3,x^2,x,1
    # Let's use basis order [1, x, x^2, x^3] for simplicity
    M = [[S[i+j] for j in range(4)] for i in range(4)]
    b = T[:4]
    # Gaussian elimination
    A = [row[:] + [b[i]] for i,row in enumerate(M)]
    for col in range(4):
        piv = max(range(col,4), key=lambda r: abs(A[r][col]))
        A[col],A[piv] = A[piv],A[col]
        pv = A[col][col]
        if abs(pv) < 1e-12:
            continue
        for r in range(4):
            if r != col:
                f = A[r][col]/pv
                for c in range(col,5):
                    A[r][c] -= f*A[col][c]
    coef = [0.0]*4
    for i in range(4):
        if abs(A[i][i]) > 1e-12:
            coef[i] = A[i][4]/A[i][i]
    d, c, b2, a = coef  # y = a x^3 + b2 x^2 + c x + d

    def f(x):
        return a*x*x*x + b2*x*x + c*x + d

    return {"y": [f(x) for x in probe["x"]]}

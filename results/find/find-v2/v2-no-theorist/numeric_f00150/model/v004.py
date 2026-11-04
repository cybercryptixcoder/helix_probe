def predict(probe):
    # f(x) is a degree-6 polynomial P(x) for |x| >= 2 (and matches at x=2, x=-2). [E2,E4,E11,E13]
    # There is a "dip" region for 1 <= x < 2: f(1)=-0.2, min ~-3.34 near 1.3, back to f(2)=36. [E10,E12]
    # There is a "dip" region for -2 < x <= -1: f(-1)=-12, min ~-12.17 near -1.1, back to f(-2)=83.2. [E14]
    # For -1 < x <= 0: f=0 (flat zero). [E8]
    # For 0 < x < 1: separate small curve, f(0.05)=4.791 ... f(0.99)=-0.1308. [E6,E8]
    # f(0)=0 (jump at 0 from small-curve side). [E8]
    # So: |x|>=2 -> P; 1<=x<2 -> dip+; -2<x<=-1 -> dip-; -1<x<=0 -> 0; 0<x<1 -> small curve.

    def solve_linear(A, b):
        n = len(A)
        M = [A[i][:] + [b[i]] for i in range(n)]
        for i in range(n):
            piv = i
            for r in range(i+1, n):
                if abs(M[r][i]) > abs(M[piv][i]):
                    piv = r
            M[i], M[piv] = M[piv], M[i]
            pv = M[i][i]
            if abs(pv) < 1e-14:
                continue
            for j in range(i, n+1):
                M[i][j] /= pv
            for r in range(n):
                if r != i and abs(M[r][i]) > 1e-15:
                    f = M[r][i]
                    for j in range(i, n+1):
                        M[r][j] -= f * M[i][j]
        return [M[i][n] for i in range(n)]

    def fit(pts, deg):
        m = deg + 1
        N = [[0.0]*m for _ in range(m)]
        rhs = [0.0]*m
        for x, y in pts:
            pw = [x**k for k in range(m)]
            for i in range(m):
                rhs[i] += pw[i]*y
                for j in range(m):
                    N[i][j] += pw[i]*pw[j]
        c = solve_linear(N, rhs)
        return lambda x: sum(c[k]*(x**k) for k in range(m))

    # Main polynomial: fit degree 6 to integer points with |x|>=2 plus x=2,-2 anchors.
    # Use clean integer data from E2, E4 (large) and negatives.
    main_pts = [
        (2,36.0),(3,913.2),(4,6364.0),(5,26805.0),(6,84676.8),(7,221368.0),
        (8,505723.2),(9,1044135.0),(10,1992220.0),
        (-2,83.2),(-3,1569.0),(-4,9472.8),(-5,36730.0),(-6,109932.0),(-7,276658.2),
        (15,23573820.0),(-15,26137995.0),(20,145577380.0),(-20,145577380.0),
        (50,33819064500.0),(-50,34880914000.0)
    ]
    P = fit(main_pts, 6)

    # Dip above 1: points from E10/E12 for 1<=x<=2
    dip_pos_pts = [
        (1.0,-0.2),(1.02,-0.6739),(1.04,-0.9428),(1.05,-1.0751),(1.06,-1.2056),
        (1.08,-1.461),(1.1,-1.7077),(1.15,-2.2766),(1.2,-2.7576),(1.3,-3.3418),
        (1.4,-3.1972),(1.45,-2.7529),(1.5,-2.0),(1.55,-0.8877),(1.6,0.6391),
        (1.7,5.1806),(1.8,12.1612),(1.9,22.1992),(1.95,28.5817),(1.98,32.9019),
        (2.0,36.0)
    ]
    Dpos = fit(dip_pos_pts, 6)

    # Dip below -1: points from E14 for -2<=x<=-1
    dip_neg_pts = [
        (-1.0,-12.0),(-1.01,-12.0352),(-1.02,-12.0668),(-1.05,-12.1378),
        (-1.1,-12.1679),(-1.2,-11.8166),(-1.25,-11.3857),(-1.3,-10.7482),
        (-1.35,-9.8736),(-1.4,-8.7292),(-1.45,-7.2797),(-1.5,-5.4875),
        (-1.55,-3.312),(-1.6,-0.7102),(-1.65,2.364),(-1.75,10.1279),
        (-1.8,14.9244),(-1.9,26.6367),(-1.95,33.6784),(-2.0,83.2)
    ]
    Dneg = fit(dip_neg_pts, 6)

    # Small positive curve 0<x<1
    small_pts = [
        (0.05,4.791),(0.1,4.5919),(0.2,4.21),(0.25,4.0205),(0.3,3.8276),(0.4,3.419),
        (0.45,3.1979),(0.5,2.9625),(0.55,2.7112),(0.6,2.4428),(0.7,1.8536),
        (0.75,1.5342),(0.8,1.2006),(0.9,0.5037),(0.95,0.1497),(0.99,-0.1308)
    ]
    S = fit(small_pts, 5)

    out = []
    for x in probe.get("x", []):
        try:
            if x >= 2 or x <= -2:
                y = P(x)
            elif x >= 1:
                y = Dpos(x)
            elif x > -1:
                if x <= 0:
                    y = 0.0
                else:
                    y = S(x)
            else:  # -2 < x <= -1
                y = Dneg(x)
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}

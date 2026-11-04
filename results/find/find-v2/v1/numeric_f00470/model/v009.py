def predict(probe):
    """f(x) = P(x) + bump(x) on (0,1), where P is a polynomial fit to E10 data
    (leading ~ x^6 with lower-order terms), bump is a negative dip vanishing at 0 and 1."""
    try:
        xs = probe.get("x", [])
        ys = []

        # Fit P(x) = a6*x^6 + a5*x^5 + a4*x^4 + a3*x^3 + a2*x^2 + a1*x + a0
        # using anchors from E10/E1 (points outside (0,1)):
        anchors = [
            (0.0, 22.28),
            (1.0, 70.35),
            (3.0, 28401.19),
            (5.0, 358938.83),
            (7.0, 1919316.07),
            (12.0, 28314372.32),
            (22.0, 586056207.82),
            (128.0, 3910458732817.44),
            (-128.0, -1178446075326.536),
        ]
        n = 7
        A = [[0.0]*n for _ in range(n)]
        b = [0.0]*n
        for xv, yv in anchors:
            pw = [xv**k for k in range(n)]
            for i in range(n):
                b[i] += pw[i]*yv
                for j in range(n):
                    A[i][j] += pw[i]*pw[j]
        M = [row[:] + [b[i]] for i, row in enumerate(A)]
        for i in range(n):
            piv = M[i][i]
            if abs(piv) < 1e-30:
                piv = 1e-30
            for j in range(i, n+1):
                M[i][j] /= piv
            for k in range(n):
                if k != i:
                    fac = M[k][i]
                    for j in range(i, n+1):
                        M[k][j] -= fac*M[i][j]
        coef = [M[i][n] for i in range(n)]

        def P(x):
            return sum(coef[k]*(x**k) for k in range(n))

        # Bump on (0,1): negative, zero at 0 and 1.
        # Anchors: B(0.25) = -3.2851 - P(0.25)
        #          B(0.5)  = -21.9553 - P(0.5)
        #          B(0.75) = -14.0279 - P(0.75)
        def bump(x):
            u = x*(1-x)
            p25 = P(0.25); p50 = P(0.5); p75 = P(0.75)
            b25 = -3.2851 - p25
            b50 = -21.9553 - p50
            b75 = -14.0279 - p75
            u25 = 0.25*0.75; u50 = 0.25; u75 = 0.25*0.75
            v25 = u25*(0.25-0.5); v50 = 0.0; v75 = u75*(0.75-0.5)
            w25 = u25*(0.25-0.5)**2; w50 = 0.0; w75 = u75*(0.75-0.5)**2
            M2 = [
                [u25, v25, w25, b25],
                [u50, v50, w50, b50],
                [u75, v75, w75, b75],
            ]
            for i in range(3):
                piv = M2[i][i]
                if abs(piv) < 1e-12:
                    piv = 1e-12
                for j in range(i, 4):
                    M2[i][j] /= piv
                for k in range(3):
                    if k != i:
                        fac = M2[k][i]
                        for j in range(i, 4):
                            M2[k][j] -= fac*M2[i][j]
            c0, c1, c2 = M2[0][3], M2[1][3], M2[2][3]
            return c0*u + c1*u*(x-0.5) + c2*u*(x-0.5)**2

        for x in xs:
            try:
                y = P(x)
                if 0 < x < 1:
                    y += bump(x)
            except Exception:
                y = None
            ys.append(y)
        return {"y": ys}
    except Exception:
        return {"y": []}

def predict(probe):
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            if x is None:
                out.append(None)
                continue
            x = float(x)
            if x >= 0:
                y = 106.06 + 111.43 * x
            else:
                ax = -x
                if ax >= 2.0:
                    y = 26.07 * ax - 25.4
                elif ax >= 1.05:
                    # trough from |x|=1.05 to |x|=2, quadratic joining linear law at 2.0
                    a = 6.37
                    t1 = 1.5 - 1.05
                    t2 = 2.0 - 1.05
                    y1 = 13.6624
                    y2 = 26.6982
                    d1 = y1 - a
                    d2 = y2 - a
                    det = t1 * t2 * t2 - t2 * t1 * t1
                    b = (d1 * t2 * t2 - d2 * t1 * t1) / det
                    c = (d2 * t1 - d1 * t2) / det
                    t = ax - 1.05
                    y = a + b * t + c * t * t
                else:
                    # near-zero fall |x| in [0,1.05]: quartic fit through dense points
                    # anchor points (ax, y): (0,106.06),(0.5,50.34),(0.85,14.04),(1.0,6.85),(1.05,6.37)
                    # use quartic through these to capture the 0.6-1.0 shape
                    pts = [(0.0, 106.06), (0.5, 50.34), (0.85, 14.04), (1.0, 6.85), (1.05, 6.37)]
                    # solve Vandermonde for coefficients c0..c4
                    n = 5
                    A = [[p[0]**k for k in range(n)] for p in pts]
                    bvec = [p[1] for p in pts]
                    # Gaussian elimination
                    M = [row[:] + [bvec[i]] for i, row in enumerate(A)]
                    for col in range(n):
                        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
                        M[col], M[piv] = M[piv], M[col]
                        pv = M[col][col]
                        if abs(pv) < 1e-12:
                            continue
                        for r in range(n):
                            if r != col:
                                fac = M[r][col] / pv
                                for cc in range(col, n + 1):
                                    M[r][cc] -= fac * M[col][cc]
                    coef = [M[i][n] / M[i][i] if abs(M[i][i]) > 1e-12 else 0.0 for i in range(n)]
                    y = sum(coef[k] * (ax ** k) for k in range(n))
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

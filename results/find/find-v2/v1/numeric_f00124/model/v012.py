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
                elif ax >= 1.07:
                    # trough from |x|=1.07 to |x|=2: cubic through dense observed points
                    pts = [
                        (1.07, 6.3684),
                        (1.10, 6.436),
                        (1.20, 7.4701),
                        (1.30, 9.0565),
                        (1.40, 11.2441),
                        (1.50, 13.6624),
                        (1.60, 16.2696),
                        (1.70, 18.8767),
                        (1.80, 21.4839),
                        (1.90, 24.0911),
                        (2.00, 26.6982),
                    ]
                    # least-squares cubic fit in t = ax
                    n = 4
                    # build normal equations
                    A = [[0.0] * n for _ in range(n)]
                    b = [0.0] * n
                    for (t, v) in pts:
                        pw = [t ** k for k in range(n)]
                        for i in range(n):
                            b[i] += pw[i] * v
                            for j in range(n):
                                A[i][j] += pw[i] * pw[j]
                    # gaussian elimination
                    M = [A[i][:] + [b[i]] for i in range(n)]
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
                else:
                    # near-zero fall |x| in [0,1.07]: quartic fit through dense points
                    pts = [(0.0, 106.06), (0.5, 50.34), (0.85, 14.04), (1.0, 6.8494), (1.07, 6.3684)]
                    n = 5
                    A = [[p[0]**k for k in range(n)] for p in pts]
                    bvec = [p[1] for p in pts]
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

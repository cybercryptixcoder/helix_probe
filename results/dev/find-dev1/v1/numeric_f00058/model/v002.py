def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        FLAT = -84.3663
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            x = float(x)
            if -32.0 <= x <= 50.0:
                ys.append(FLAT)
            elif x > 50.0:
                # cubic in d = x - 50, anchored to positive-side points
                d = x - 50.0
                # points: (2, 428.046), (10, 6838.9942), (14, 15971.2842), (78, 258083.9783)
                # fit cubic c3 d^3 + c2 d^2 + c1 d + FLAT
                import math
                pts = [(2.0, 428.046), (10.0, 6838.9942), (14.0, 15971.2842), (78.0, 258083.9783)]
                # Solve 4x4 linear system for c1,c2,c3,c0 with c0=FLAT
                # Build normal equations manually
                # rows: [d, d^2, d^3], rhs = y - FLAT
                A = [[p[0], p[0]**2, p[0]**3] for p in pts]
                b = [p[1] - FLAT for p in pts]
                # Gaussian elimination
                M = [row[:] + [bb] for row, bb in zip(A, b)]
                n = 3
                for i in range(n):
                    piv = max(range(i, n), key=lambda r: abs(M[r][i]))
                    M[i], M[piv] = M[piv], M[i]
                    if abs(M[i][i]) < 1e-12:
                        continue
                    for r in range(i+1, n):
                        f = M[r][i] / M[i][i]
                        for c in range(i, n+1):
                            M[r][c] -= f * M[i][c]
                coef = [0.0]*n
                for i in range(n-1, -1, -1):
                    s = M[i][n]
                    for j in range(i+1, n):
                        s -= M[i][j]*coef[j]
                    coef[i] = s / M[i][i] if abs(M[i][i]) > 1e-12 else 0.0
                c1, c2, c3 = coef
                ys.append(c3*d**3 + c2*d**2 + c1*d + FLAT)
            else:
                # x < -32: cubic in d = |x| - 32, anchored to negative-side points
                a = -x
                d = a - 32.0
                # points: (32, 44756.7193), (68, 203265.332), (96, 326549.8085)
                # plus plateau edge (0, FLAT)
                pts = [(0.0, FLAT), (32.0, 44756.7193), (68.0, 203265.332), (96.0, 326549.8085)]
                A = [[p[0], p[0]**2, p[0]**3] for p in pts]
                b = [p[1] - FLAT for p in pts]
                M = [row[:] + [bb] for row, bb in zip(A, b)]
                n = 3
                for i in range(n):
                    piv = max(range(i, n), key=lambda r: abs(M[r][i]))
                    M[i], M[piv] = M[piv], M[i]
                    if abs(M[i][i]) < 1e-12:
                        continue
                    for r in range(i+1, n):
                        f = M[r][i] / M[i][i]
                        for c in range(i, n+1):
                            M[r][c] -= f * M[i][c]
                coef = [0.0]*n
                for i in range(n-1, -1, -1):
                    s = M[i][n]
                    for j in range(i+1, n):
                        s -= M[i][j]*coef[j]
                    coef[i] = s / M[i][i] if abs(M[i][i]) > 1e-12 else 0.0
                c1, c2, c3 = coef
                ys.append(c3*d**3 + c2*d**2 + c1*d + FLAT)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}

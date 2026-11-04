def predict(probe):
    try:
        xs = probe.get("x", [])
    except Exception:
        return {"y": []}

    # Cubic coefficient for |x| >= 2
    a = -3.9

    # Near-zero region fit (|x| < 2). Use a cubic polynomial fit through
    # the observed small-|x| points from E1 and E2 (least-squares-ish,
    # hand-fit to match the bumpy asymmetric shape).
    # Points used (x, y):
    # (-1.9,26.8241),(-1.5,14.0934),(-1.2,9.3243),(-0.9,3.809),(-0.7,3.8806),
    # (-0.5,2.1535),(-0.3,2.0274),(-0.1,4.0416),(0,3.0185),(0.1,4.4585),
    # (0.3,4.3917),(0.5,1.7151),(0.7,3.6142),(0.9,3.0233),(1,2.8803),
    # (1.2,-2.5089),(1.5,-5.5345),(1.9,-18.7823)
    # Fit a degree-5 polynomial to capture the wiggles.
    coeffs = _fit_poly()

    def near(x):
        # Horner evaluation
        y = 0.0
        for c in coeffs:
            y = y * x + c
        return y

    out = []
    for x in xs:
        try:
            xf = float(x)
        except Exception:
            out.append(None)
            continue
        try:
            if abs(xf) >= 2.0:
                out.append(a * xf ** 3)
            else:
                out.append(near(xf))
        except Exception:
            out.append(None)
    return {"y": out}


def _fit_poly():
    # Least-squares polynomial fit (degree 5) through near-zero data points.
    # Implemented with normal equations using pure Python.
    pts = [
        (-1.9, 26.8241), (-1.5, 14.0934), (-1.2, 9.3243), (-0.9, 3.809),
        (-0.7, 3.8806), (-0.5, 2.1535), (-0.3, 2.0274), (-0.1, 4.0416),
        (0.0, 3.0185), (0.1, 4.4585), (0.3, 4.3917), (0.5, 1.7151),
        (0.7, 3.6142), (0.9, 3.0233), (1.0, 2.8803), (1.2, -2.5089),
        (1.5, -5.5345), (1.9, -18.7823),
    ]
    deg = 5
    n = deg + 1
    # Build normal equations A^T A c = A^T y
    ATA = [[0.0] * n for _ in range(n)]
    ATy = [0.0] * n
    for x, y in pts:
        powers = [x ** k for k in range(n)]
        for i in range(n):
            ATy[i] += powers[i] * y
            for j in range(n):
                ATA[i][j] += powers[i] * powers[j]
    # Solve via Gaussian elimination
    M = [row[:] + [ATy[i]] for i, row in enumerate(ATA)]
    for col in range(n):
        # pivot
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        if abs(pv) < 1e-12:
            continue
        for j in range(col, n + 1):
            M[col][j] /= pv
        for r in range(n):
            if r != col:
                factor = M[r][col]
                if factor != 0.0:
                    for j in range(col, n + 1):
                        M[r][j] -= factor * M[col][j]
    # coeffs in descending order for Horner: c_deg, ..., c_0
    c = [M[i][n] for i in range(n)]
    return list(reversed(c))

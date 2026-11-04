def predict(probe):
    try:
        xs = probe.get("x", [])
    except Exception:
        return {"y": []}

    a = -3.9
    coeffs = _fit_poly()

    def near(x):
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
            if abs(xf) >= 2.6:
                out.append(a * xf ** 3)
            else:
                out.append(near(xf))
        except Exception:
            out.append(None)
    return {"y": out}


def _fit_poly():
    pts = [
        (-2.4, 50.782), (-2.2, 38.2072), (-2.1, 33.2797), (-2.05, 32.8869),
        (-2.0, 29.9635), (-1.99, 28.4279), (-1.95, 29.2889), (-1.9, 27.3775),
        (-1.8, 22.1923), (-1.7, 19.7649), (-1.6, 15.7882), (-1.5, 11.5506),
        (-1.4, 12.0303), (-1.3, 9.5526), (-1.2, 7.223), (-1.1, 7.1396),
        (-1.0, 4.9395), (-0.95, 3.5844), (-0.9, 4.8425),
        (-0.7, 3.8806), (-0.5, 2.1535), (-0.3, 2.0274), (-0.1, 4.0416),
        (0.0, 3.0185), (0.1, 4.4585), (0.3, 4.3917), (0.5, 1.7151),
        (0.7, 3.6142), (0.9, 3.0233), (1.0, 2.8803), (1.2, -2.5089),
        (1.5, -5.5345), (1.9, -18.7823),
    ]
    deg = 6
    n = deg + 1
    ATA = [[0.0] * n for _ in range(n)]
    ATy = [0.0] * n
    for x, y in pts:
        powers = [x ** k for k in range(n)]
        for i in range(n):
            ATy[i] += powers[i] * y
            for j in range(n):
                ATA[i][j] += powers[i] * powers[j]
    M = [row[:] + [ATy[i]] for i, row in enumerate(ATA)]
    for col in range(n):
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
    c = [M[i][n] for i in range(n)]
    return list(reversed(c))

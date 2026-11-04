def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                y = _f(x)
            except Exception:
                y = None
            ys.append(y)
        return {"y": ys}
    except Exception:
        return {"y": []}


def _base(x):
    # x^3 + 2^x + 22
    return x**3 + 2.0**x + 22.0


def _f(x):
    # Large |x|: use polynomial fit through E1/E10 anchors
    if abs(x) > 20:
        return _poly_large(x)
    # Moderate |x|: base formula
    y = _base(x)
    # (0,1) dip: roughly -1 additive, vanishing at endpoints
    if 0 < x < 1:
        # dip observed ~ -1 at 0.1..0.9, ~-1.01 near 0.01/0.99
        # model as -1 * smooth window that is ~1 in interior
        # simple: -1 constant (endpoints handled by base at 0 and 1)
        y += -1.0
    return y


def _poly_large(x):
    # Fit polynomial to large-|x| anchors from E1/E10
    anchors = [
        (22.0, 586056207.82),
        (30.0, None),  # skip
        (40.0, None),
        (64.0, None),
        (100.0, None),
        (128.0, 3910458732817.44),
        (-128.0, -1178446075326.536),
        (-100.0, None),
        (-64.0, None),
        (-40.0, None),
        (-30.0, -845065562.49),
        (-22.0, -180438045.506),
        (-16.0, -37069161.656),
        (-12.0, -8903749.956),
        (-9.0, -2148291.995),
        (-7.0, -623588.531),
        (-5.0, -120305.515),
        (-3.0, -10245.411),
        (3.0, 28401.19),
        (5.0, 358938.83),
        (7.0, 1919316.07),
        (9.0, 6727933.75),
        (12.0, 28314372.32),
        (16.0, 119254427.2),
    ]
    pts = [(a, b) for a, b in anchors if b is not None]
    # Use degree-6 least squares
    n = 7
    A = [[0.0]*n for _ in range(n)]
    rhs = [0.0]*n
    for xv, yv in pts:
        pw = [xv**k for k in range(n)]
        for i in range(n):
            rhs[i] += pw[i]*yv
            for j in range(n):
                A[i][j] += pw[i]*pw[j]
    M = [row[:] + [rhs[i]] for i, row in enumerate(A)]
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
    return sum(coef[k]*(x**k) for k in range(n))

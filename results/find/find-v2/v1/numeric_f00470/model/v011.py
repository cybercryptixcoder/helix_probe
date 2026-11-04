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
    return x**3 + 2.0**x + 22.0


def _dip(x):
    # Symmetric dip on (0,1), zero at endpoints, minimum ~-44 at x=0.5.
    # Anchors (distance from 0.5): g(0.5)=-44, g(0.4)=-40, g(0.25)=-27,
    # g(0.15)=-13.6, g(0.1)=-11, g(0.05)=-6.6, g(0.02)=-2.7, g(0.01)=-1.01
    # Fit as a function of t = |x-0.5| in [0,0.5].
    t = abs(x - 0.5)
    # Use a smooth shape: -44 * (1 - (2t)^p) style, but data is steeper near center.
    # Try g(t) = -44 * (1 - (2t)^2)^q form; fit q roughly.
    # At t=0.4 (x=0.1): 2t=0.8, want -11 => (1-0.64)^q = 11/44=0.25 => 0.36^q=0.25 => q~1.35
    # At t=0.25 (x=0.25): 2t=0.5, (1-0.25)^1.35=0.75^1.35=0.68 => -30 (obs -27, ok)
    # At t=0.1 (x=0.4): 2t=0.2, (1-0.04)^1.35=0.946 => -41.6 (obs -40, ok)
    # At t=0.35 (x=0.15): 2t=0.7, (1-0.49)^1.35=0.51^1.35=0.40 => -17.6 (obs -13.6, a bit off)
    # At t=0.45 (x=0.05): 2t=0.9, (1-0.81)^1.35=0.19^1.35=0.106 => -4.7 (obs -6.6)
    # At t=0.48 (x=0.02): 2t=0.96, (1-0.9216)^1.35=0.0784^1.35=0.031 => -1.4 (obs -2.7)
    # Reasonable approximation. Refine with a blend.
    if t >= 0.5:
        return 0.0
    val = 1.0 - (2.0*t)**2
    if val < 0:
        val = 0.0
    return -44.0 * (val ** 1.35)


def _f(x):
    if abs(x) > 22:
        return _poly_large(x)
    y = _base(x)
    if 0 < x < 1:
        y += _dip(x)
    return y


def _poly_large(x):
    anchors = [
        (22.0, 586056207.82),
        (128.0, 3910458732817.44),
        (-128.0, -1178446075326.536),
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

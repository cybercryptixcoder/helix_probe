import math

def predict(probe):
    # f(x) = 0 outside [-0.8, ~0.8] [E2,E3,E4,E5,E7,E9]
    # Left edge: f=0 for x<=-0.81, f(-0.8)=-5.252, so nonzero starts at -0.8 [E10]
    # Right edge: f(0.75)=-2.2062, f(0.9)=0; boundary somewhere in (0.75,0.9) [E4]
    # Inside: smooth curve, min at x=-0.8, local max near x=0.25, then falls [E4,E6,E8]
    # Values look like a smooth function; fit a polynomial through known points.
    # Known points (x,y):
    pts = [
        (-0.8, -5.252), (-0.79, -5.1815), (-0.78, -5.1117), (-0.77, -5.0426),
        (-0.76, -4.9741), (-0.75, -4.9062), (-0.74, -4.8391), (-0.73, -4.7726),
        (-0.72, -4.7067), (-0.71, -4.6415), (-0.7, -4.577), (-0.69, -4.5131),
        (-0.68, -4.4499), (-0.67, -4.3874), (-0.65, -4.2643), (-0.62, -4.0845),
        (-0.6, -3.968), (-0.58, -3.8541), (-0.55, -3.6883), (-0.52, -3.5283),
        (-0.5, -3.425), (-0.48, -3.3243), (-0.45, -3.1783), (-0.42, -3.0381),
        (-0.4, -2.948), (-0.38, -2.8605), (-0.35, -2.7342), (-0.32, -2.6139),
        (-0.3, -2.537), (-0.28, -2.4627), (-0.25, -2.3563), (-0.22, -2.2557),
        (-0.2, -2.192), (-0.18, -2.1309), (-0.15, -2.0442), (-0.12, -1.9635),
        (-0.1, -1.913), (-0.08, -1.8651), (-0.05, -1.7982), (-0.02, -1.7373),
        (0.0, -1.7), (0.02, -1.6653), (0.05, -1.6182), (0.08, -1.5771),
        (0.1, -1.553), (0.15, -1.5042), (0.2, -1.472), (0.25, -1.4562),
        (0.35, -1.4742), (0.5, -1.625), (0.6, -1.808), (0.65, -1.9242),
        (0.75, -2.2062),
    ]
    # Fit a polynomial (degree ~6) to these points once, lazily.
    # Use least squares via normal equations with numpy-free Gaussian elimination.
    if not hasattr(predict, "_coef"):
        deg = 6
        n = deg + 1
        # Build normal equations A^T A c = A^T b
        A = [[x**k for k in range(n)] for (x, y) in pts]
        b = [y for (x, y) in pts]
        # M = A^T A, v = A^T b
        M = [[sum(A[i][r] * A[i][c] for i in range(len(A))) for c in range(n)] for r in range(n)]
        v = [sum(A[i][r] * b[i] for i in range(len(A))) for r in range(n)]
        # Gaussian elimination
        for col in range(n):
            piv = max(range(col, n), key=lambda r: abs(M[r][col]))
            M[col], M[piv] = M[piv], M[col]
            v[col], v[piv] = v[piv], v[col]
            if abs(M[col][col]) < 1e-12:
                continue
            for r in range(n):
                if r != col:
                    factor = M[r][col] / M[col][col]
                    for c in range(col, n):
                        M[r][c] -= factor * M[col][c]
                    v[r] -= factor * v[col]
        coef = [v[i] / M[i][i] if abs(M[i][i]) > 1e-12 else 0.0 for i in range(n)]
        predict._coef = coef
    coef = predict._coef

    def poly(x):
        return sum(coef[k] * x**k for k in range(len(coef)))

    # Right boundary: find where poly crosses 0 in (0.75, 0.9); fallback 0.85
    # Since poly may not be monotone, just taper linearly from 0.75 to 0.85 (?)
    def f(x):
        if x < -0.8 or x > 0.85:
            return 0.0
        if x == -0.8:
            return -5.252
        if x > 0.75:
            # taper from -2.2062 at 0.75 to 0 at 0.85 (?)
            t = (0.85 - x) / (0.85 - 0.75)
            return -2.2062 * t
        return poly(x)

    return {"y": [f(x) for x in probe["x"]]}

def predict(probe):
    # Hypothesis: f(x) is roughly quadratic in x, with a different (smaller)
    # coefficient regime for x < 0 vs x > 0 [E1].
    # Check E1: x=88.2 -> 9933.99 ; x=66 -> 7460.29 ; x=72.7 -> 8206.85
    #   ratio y/x^2: 1.277, 1.713, 1.553 -- not constant, so not pure quadratic.
    # Try cubic-ish / mixed. Let's fit a polynomial through the data.
    # We'll use a simple degree-3 polynomial fit on the single experiment.
    # Points (x, y):
    # (88.2,9933.9859),(66.0,7460.2885),(-20.3,503.8102),(-61.7,1583.1784),
    # (2.9,429.1934),(-24.3,608.097),(72.7,8206.8548),(-50.4,1288.5682),
    # (-6.0,130.985),(21.3,2479.4652)
    # Note: x=2.9 -> 429 is large for small x, and x=-6 -> 131.
    # Suggests maybe |x| or x^2 plus something. Let's check y vs x^2:
    # x^2: 7779,4356,412,3807,8.4,590,5285,2540,36,454
    # y/x^2: 1.277,1.713,1.222,0.416,51.1,1.03,1.553,0.507,3.64,5.46
    # Not clean. Try y vs x^2 + c*|x|? Hard from one experiment.
    # Best guess: fit cubic polynomial via least squares using numpy-free solve.
    import math
    xs = [88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3]
    ys = [9933.9859,7460.2885,503.8102,1583.1784,429.1934,608.097,
          8206.8548,1288.5682,130.985,2479.4652]
    # Build normal equations for degree 3
    n = 4
    A = [[0.0]*n for _ in range(n)]
    b = [0.0]*n
    for x, y in zip(xs, ys):
        p = [1.0, x, x*x, x*x*x]
        for i in range(n):
            b[i] += p[i]*y
            for j in range(n):
                A[i][j] += p[i]*p[j]
    # Gaussian elimination
    for i in range(n):
        piv = max(range(i,n), key=lambda r: abs(A[r][i]))
        A[i],A[piv] = A[piv],A[i]
        b[i],b[piv] = b[piv],b[i]
        if abs(A[i][i]) < 1e-12:
            continue
        for r in range(i+1,n):
            f = A[r][i]/A[i][i]
            for c in range(i,n):
                A[r][c] -= f*A[i][c]
            b[r] -= f*b[i]
    coef = [0.0]*n
    for i in range(n-1,-1,-1):
        if abs(A[i][i]) < 1e-12:
            coef[i] = 0.0
            continue
        s = b[i]
        for j in range(i+1,n):
            s -= A[i][j]*coef[j]
        coef[i] = s/A[i][i]
    def f(x):
        return coef[0] + coef[1]*x + coef[2]*x*x + coef[3]*x*x*x
    out = {}
    out["y"] = [f(x) for x in probe["x"]]
    return out

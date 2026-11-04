def predict(probe):
    # Observations:
    # - Flat region: f(x) = -84.3663 for x in roughly [-51, 30+] [E1, E2]
    #   E2 shows flat extends at least to x=30, and down to x=-51.
    # - Outside flat region, output grows large positive on both sides [E1]
    #   x=88.2 -> 104398.3, x=66.0 -> 21806.0, x=72.7 -> 44545.8, x=-61.7 -> 34659.9
    #   x=-55 -> 9693.7, x=-52 -> 1853.9 [E2]
    # - The flat region is asymmetric: left edge ~-51, right edge >30 (unknown) [E2]
    # - Behavior outside looks like |x|^3-ish growth on both sides but not symmetric [E1]
    # Hypothesis (?): f(x) = -84.3663 on [-51, R], else cubic-ish in x.
    # Fit cubic a*x^3+b*x^2+c*x+d to outside points.
    import math
    # Outside points from E1+E2:
    # (88.2,104398.2986),(66,21805.9764),(-61.7,34659.9424),(72.7,44545.8355),
    # (-55,9693.6736),(-52,1853.9413)
    # Solve least squares cubic via normal equations (4x4).
    pts = [(88.2,104398.2986),(66.0,21805.9764),(-61.7,34659.9424),
           (72.7,44545.8355),(-55.0,9693.6736),(-52.0,1853.9413)]
    # Build normal equations
    n = 4
    A = [[0.0]*n for _ in range(n)]
    b = [0.0]*n
    for x,y in pts:
        row = [x**3, x**2, x, 1.0]
        for i in range(n):
            for j in range(n):
                A[i][j] += row[i]*row[j]
            b[i] += row[i]*y
    # Gaussian elimination
    M = [A[i][:]+[b[i]] for i in range(n)]
    for i in range(n):
        p = max(range(i,n), key=lambda r: abs(M[r][i]))
        M[i],M[p] = M[p],M[i]
        if abs(M[i][i]) < 1e-12:
            continue
        for r in range(i+1,n):
            f = M[r][i]/M[i][i]
            for c in range(i,n+1):
                M[r][c] -= f*M[i][c]
    coef = [0.0]*n
    for i in range(n-1,-1,-1):
        if abs(M[i][i]) < 1e-12:
            coef[i] = 0.0
            continue
        s = M[i][n]
        for j in range(i+1,n):
            s -= M[i][j]*coef[j]
        coef[i] = s/M[i][i]
    a,b_,c,d = coef
    # Flat region bounds (?): left ~-51, right unknown but >30
    LEFT = -51.0
    RIGHT = 50.0  # ? guess
    def f(x):
        if LEFT < x < RIGHT:
            return -84.3663
        return a*x*x*x + b_*x*x + c*x + d
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            out.append(f(x))
        except Exception:
            out.append(None)
    return {"y": out}

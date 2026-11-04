def predict(probe):
    # Model: y = max(floor, g(x)), floor = -84.3663 (constant dead zone).
    # Dead zone: |x| below ~50 -> -84.3663 [E1..E10]
    # Outside dead zone, g(x) grows with |x|, asymmetric (neg x larger than pos x) [E1..E10]
    # Shape: looks like a smooth monotone-in-|x| curve, roughly quadratic-ish at large |x|
    #   but with a steep rise near the dead-zone edge. Fit a quartic in x (even+odd terms)
    #   to capture both the steep near-edge rise and the large-|x| curvature.
    # Use all non-floor points from the notebook.
    pts = [
        (88.2,104398.3),(66,21806.0),(-61.7,34659.9),(72.7,44545.8),
        (104.5,167339.9),(65.5,20347.3),(-63.9,44316.4),(104.9,168884.5),(123.6,241093.6),(79.4,70417.5),(103.0,161547.7),(-55.8,11784.3),
        (58.8,5395.5),(102.1,158072.4),(-102.2,212952.0),(105.7,171973.7),(119.5,225261.7),
        (93.5,124864.0),(-61.3,33041.0),(78.1,65397.7),(-124.4,310698.9),(56.2,2268.1),(83.2,85091.1),
        (-127.7,325228.9),(94.1,127180.8),(-65.6,51801.5),(94.8,129883.9),(-79.1,111242.3),(-66.9,57525.5),(119.7,226033.9),
        (77.6,63466.9),(-107.4,235847.7),(110.8,191667.1),(-100.1,203705.6),(52.9,802.1),
        (80.5,74665.1),(118.7,222172.5),(-53.7,6296.5),
        (-79.5,113003.5),(-80.2,116085.6),(-105.0,225280.4),(65.9,21514.2),(96.5,136448.3),(108.4,182399.6),(87.7,102467.6),
        (101.9,157300.2),(108.3,182013.4),(52.6,677.4),(-57.4,17256.2),(79.8,71962.1),(89.5,109418.2),(101.1,154211.0),
        (115.1,208271.3),(127.0,254222.5),(106.7,175835.1),(75.1,53813.3),(-106.9,233646.1),
    ]
    # Basis: [x^4, x^3, x^2, x, 1]
    def basis(x):
        return [x**4, x**3, x*x, x, 1.0]
    m = 5
    M = [[0.0]*m for _ in range(m)]
    rhs = [0.0]*m
    for x, y in pts:
        b = basis(x)
        for i in range(m):
            rhs[i] += b[i]*y
            for j in range(m):
                M[i][j] += b[i]*b[j]
    def solve(M, rhs):
        n = len(rhs)
        A = [row[:] + [rhs[i]] for i, row in enumerate(M)]
        for col in range(n):
            piv = max(range(col, n), key=lambda r: abs(A[r][col]))
            A[col], A[piv] = A[piv], A[col]
            if abs(A[col][col]) < 1e-12:
                continue
            for r in range(n):
                if r != col:
                    f = A[r][col]/A[col][col]
                    for c in range(col, n+1):
                        A[r][c] -= f*A[col][c]
        return [A[i][n]/A[i][i] if abs(A[i][i]) > 1e-12 else 0.0 for i in range(n)]
    c4, c3, c2, c1, c0 = solve(M, rhs)
    floor = -84.3663
    def f(x):
        try:
            v = c4*x**4 + c3*x**3 + c2*x*x + c1*x + c0
            return max(floor, v)
        except Exception:
            return None
    xs = probe.get("x", [])
    return {"y": [f(x) for x in xs]}

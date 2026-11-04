def predict(probe):
    # Observations:
    # - Flat region: f(x) = -84.3663 for x in [-51, 50] [E1,E2,E3,E4,E5]
    #   E2: flat down to -51, growth at -52. E4: flat through 50, growth at 55.
    # - Outside flat region, output grows large positive on both sides [E1,E3,E4,E5]
    #   Right: 55->1674.95, 58.8->5395.54, 60->6838.99, 62->10136.59, 64->15971.28,
    #          65->18888.63, 65.5->20347.30, 66->21805.98, 72.7->44545.84,
    #          79.4->70417.55, 88.2->104398.30, 102.1->158072.44, 103->161547.75,
    #          104.5->167339.92, 104.9->168884.50, 105.7->171973.66,
    #          119.5->225261.66, 123.6->241093.60
    #   Left: -52->1853.94, -55->9693.67, -55.8->11784.27, -61.7->34659.94,
    #         -63.9->44316.42, -102.2->212951.97
    # - Growth is cubic-ish, asymmetric (left steeper than right at same |x|).
    #   Fit separate cubics on each side using all points.
    import math

    R = [(55.0,1674.9487),(58.8,5395.5436),(60.0,6838.9942),(62.0,10136.592),
         (64.0,15971.2842),(65.0,18888.6303),(65.5,20347.3034),
         (66.0,21805.9764),(72.7,44545.8355),(79.4,70417.5454),
         (88.2,104398.2986),(102.1,158072.4431),(103.0,161547.7474),
         (104.5,167339.9212),(104.9,168884.5009),(105.7,171973.6603),
         (119.5,225261.6598),(123.6,241093.6017)]
    L = [(-52.0,1853.9413),(-55.0,9693.6736),(-55.8,11784.2688),
         (-61.7,34659.9424),(-63.9,44316.4176),(-102.2,212951.9694)]

    def fit_cubic(pts):
        n = 4
        A = [[0.0]*n for _ in range(n)]
        b = [0.0]*n
        for x,y in pts:
            row = [x**3, x**2, x, 1.0]
            for i in range(n):
                for j in range(n):
                    A[i][j] += row[i]*row[j]
                b[i] += row[i]*y
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
        return coef

    cr = fit_cubic(R)
    cl = fit_cubic(L)

    LEFT = -51.0
    RIGHT = 50.0

    def f(x):
        if LEFT <= x <= RIGHT:
            return -84.3663
        if x > RIGHT:
            a,b_,c,d = cr
            return a*x*x*x + b_*x*x + c*x + d
        a,b_,c,d = cl
        return a*x*x*x + b_*x*x + c*x + d

    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            out.append(f(x))
        except Exception:
            out.append(None)
    return {"y": out}

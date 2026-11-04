def predict(probe):
    # Beliefs:
    # - f is flat at -84.3663 on [-51.1, 50.9] inclusive [E2,E4,E6,E8,E10]
    # - Right edge: flat through 50.9, then LINEAR ramp slope ~416.3/unit
    #   from 50.9 to 51.5 (f(50.9)=-29.1516, f(51.5)=220.2289) [E14,E16]
    # - Right ramp continues LINEARLY well past 51.5: E14/E16 show constant
    #   increments of ~41.56 per 0.1 up to 53.0, then ~166.3 per 0.5 to 54,
    #   then ~207.8 per 0.5 to 55. So it's linear from 50.9 to ~53.0, then
    #   curves upward into the cubic region [E14,E16]
    # - Left edge: flat through -51.1; f(-51.2)=-84.3663, f(-51.3)=24.6704,
    #   f(-51.4)=285.9948, f(-51.5)=547.3193: increments 109.34, 261.32, 261.32
    #   then constant 261.32 per 0.1 up to -52.0, then ~261.32 per 0.2 [E18]
    #   So left ramp is LINEAR with slope ~2613.2/unit starting at -51.2,
    #   continuing linearly through the whole near-edge region [E18]
    # - Beyond the ramp, growth is cubic-ish; left steeper than right [E1,E3,E5,E7,E9]
    import math

    R = [(51.0,12.4118),(51.5,220.2289),(52.0,428.046),(52.5,635.8631),
         (53.0,843.6803),(53.5,1051.4974),(54.0,1259.3145),
         (55.0,1674.9487),(56.2,2268.0673),(58.8,5395.5436),
         (60.0,6838.9942),(62.0,10136.592),(64.0,15971.2842),
         (65.0,18888.6303),(65.5,20347.3034),(66.0,21805.9764),
         (72.7,44545.8355),(78.1,65397.6613),(79.4,70417.5454),
         (83.2,85091.0525),(88.2,104398.2986),(93.5,124863.9796),
         (102.1,158072.4431),(103.0,161547.7474),(104.5,167339.9212),
         (104.9,168884.5009),(105.7,171973.6603),(119.5,225261.6598),
         (123.6,241093.6017)]
    L = [(-51.5,547.3193),(-52.0,1853.9413),(-52.5,3160.5633),
         (-53.0,4467.1854),(-53.5,5773.8074),
         (-55.0,9693.6736),(-55.8,11784.2688),(-61.3,33040.9864),
         (-61.7,34659.9424),(-63.9,44316.4176),
         (-102.2,212951.9694),(-124.4,310698.9472)]

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

    FLAT = -84.3663
    LEFT = -51.1
    RIGHT = 50.9

    # Right ramp: linear from 50.9 to 53.0 (slope ~415.6/unit),
    # then smooth curve up to 55 where cubic takes over.
    R_RAMP = [(50.9, -29.1516), (51.0, 12.4118), (51.1, 53.9752),
              (51.2, 95.5386), (51.3, 137.1021), (51.4, 178.6655),
              (51.5, 220.2289), (51.6, 261.7923), (51.7, 303.3558),
              (51.8, 344.9192), (51.9, 386.4826), (52.0, 428.046),
              (52.2, 511.1729), (52.4, 594.2997), (52.6, 677.4266),
              (52.8, 760.5534), (53.0, 843.6803), (53.5, 1051.4974),
              (54.0, 1259.3145), (55.0, 1674.9487)]
    # Left ramp: linear from -51.2 (f=-84.3663) with slope ~2613.2/unit,
    # through -52.0 (f=1853.9413), continuing to -53.5 then into cubic.
    L_RAMP = [(-53.5, 5773.8074), (-53.0, 4467.1854), (-52.5, 3160.5633),
              (-52.0, 1853.9413), (-51.9, 1592.6169), (-51.8, 1331.2925),
              (-51.7, 1069.9681), (-51.6, 808.6437), (-51.5, 547.3193),
              (-51.4, 285.9948), (-51.3, 24.6704), (-51.2, FLAT),
              (-51.1, FLAT)]

    def interp(pts, x):
        if x <= pts[0][0]:
            (x0,y0),(x1,y1) = pts[0],pts[1]
        elif x >= pts[-1][0]:
            (x0,y0),(x1,y1) = pts[-2],pts[-1]
        else:
            for i in range(len(pts)-1):
                if pts[i][0] <= x <= pts[i+1][0]:
                    (x0,y0),(x1,y1) = pts[i],pts[i+1]
                    break
        if x1 == x0:
            return y0
        return y0 + (y1-y0)*(x-x0)/(x1-x0)

    def f(x):
        if LEFT <= x <= RIGHT:
            return FLAT
        if x > RIGHT:
            if x <= 55.0:
                return interp(R_RAMP, x)
            a,b_,c,d = cr
            return a*x*x*x + b_*x*x + c*x + d
        # left side
        if x >= -53.5:
            return interp(L_RAMP, x)
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

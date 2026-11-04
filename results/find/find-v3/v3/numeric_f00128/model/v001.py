def predict(probe):
    # Hypothesis: f(x) is approximately a cubic: y ≈ a*x^3 + b*x + c
    # Fit from E1 data. Let's estimate.
    # Points: (88.2,-1479.38),(66,-1104.2),(-20.3,139.62),(-61.7,419.49),
    # (2.9,-37.79),(-24.3,166.66),(72.7,-1217.43),(-50.4,343.10),
    # (-6,42.95),(21.3,-348.78)
    # Try odd function: y ≈ a*x^3 + b*x (no constant, since f(0)≈0?)
    # Check: at x=2.9, y=-37.79; at x=-6, y=42.95. Roughly odd-ish.
    # Let's just fit a*x^3+b*x via least squares mentally... hard.
    # Alternative: y looks like -0.00215*x^3 roughly? 
    # 88.2^3=686128, *-0.002156=-1479. yes! a≈-0.002156
    # 66^3=287496 *-0.002156=-619.8, but observed -1104. Not pure cubic.
    # Try a*x^3+b*x: at 66: 287496a+66b=-1104.2
    # at 88.2: 686128a+88.2b=-1479.38
    # Solve: from first b=(-1104.2-287496a)/66
    # plug: 686128a+88.2*(-1104.2-287496a)/66=-1479.38
    # 686128a + 1.33636*(-1104.2-287496a) = -1479.38
    # 686128a -1475.6 -384188a = -1479.38
    # 301940a = -3.78 => a=-1.25e-5. Then b=(-1104.2+3.6)/66=-16.68
    # Check x=2.9: -1.25e-5*24.4 -16.68*2.9 = -0.0003-48.4=-48.4 vs -37.79. off.
    # Hmm. Let's try including x^2? Or maybe it's tanh-based MLP.
    # Given MLP approximation, likely smooth. Let's fit cubic a*x^3+b*x^2+c*x+d.
    # Use several points. This is getting complex; use numpy-free least squares.
    import itertools
    xs=[88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3]
    ys=[-1479.3769,-1104.1996,139.6237,419.4911,-37.7888,166.664,-1217.4288,343.1022,42.9545,-348.775]
    # Build normal equations for cubic
    n=4
    A=[[0.0]*n for _ in range(n)]
    B=[0.0]*n
    for x,y in zip(xs,ys):
        p=[x**k for k in range(n)]
        for i in range(n):
            B[i]+=p[i]*y
            for j in range(n):
                A[i][j]+=p[i]*p[j]
    # Gaussian elimination
    M=[row[:]+[B[i]] for i,row in enumerate(A)]
    for i in range(n):
        piv=M[i][i]
        if abs(piv)<1e-12: continue
        for j in range(i+1,n):
            f=M[j][i]/piv
            for k in range(i,n+1):
                M[j][k]-=f*M[i][k]
    coef=[0.0]*n
    for i in range(n-1,-1,-1):
        s=M[i][n]
        for j in range(i+1,n):
            s-=M[i][j]*coef[j]
        coef[i]=s/M[i][i] if abs(M[i][i])>1e-12 else 0.0
    def f(x):
        return sum(coef[k]*x**k for k in range(n))
    return {"y":[f(x) for x in probe["x"]]}

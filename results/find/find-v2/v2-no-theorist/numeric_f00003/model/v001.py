def predict(probe):
    # Observations:
    # - For x <= -20 (approx), f(x) is a smooth increasing function of x (quadratic-like).
    #   E2: f(-120)=22280, f(-100)=15883, f(-80)=9582, f(-60)=4736, f(-40)=1532, f(-30)=548.
    # - For -20 < x < 5 (approx), f(x) is constant at -20.4469.
    #   E2: f(-20)=-20.4469, f(-10)=-20.4469, f(-5)=-20.4469, f(-1)=-20.4469, f(0)=-20.4469, f(1)=-20.4469.
    #   E1: f(-6.0)=-20.4469.
    # - For x >= 5 (approx), f(x) is a smooth increasing quadratic-like function.
    #   E2: f(5)=48.39, f(10)=650.48, f(20)=1914.24, f(30)=3458.11, f(40)=5505.53, f(60)=10959.96, f(80)=18320.40, f(100)=26939.45.
    #   E1: f(2.9)=-20.4469 (still in flat region), f(21.3)=2091.93, f(66.0)=12950.84, f(72.7)=15366.07, f(88.2)=21854.21.
    # - Note f(-20.3)=-15.8672 in E1, slightly above -20.4469, suggesting the flat region boundary is near -20.
    #   Actually f(-20)=-20.4469 but f(-20.3)=-15.8672, so the transition is between -20.3 and -20.
    # - f(-24.3)=166.21, f(-50.4)=2995.40, f(-61.7)=5086.13.
    # Fit quadratics on each side.

    import math

    def quad_fit(xs, ys):
        # least squares fit y = a*x^2 + b*x + c
        n = len(xs)
        Sx = sum(xs); Sx2 = sum(x*x for x in xs); Sx3 = sum(x**3 for x in xs); Sx4 = sum(x**4 for x in xs)
        Sy = sum(ys); Sxy = sum(x*y for x,y in zip(xs,ys)); Sx2y = sum(x*x*y for x,y in zip(xs,ys))
        # Solve normal equations
        # [Sx4 Sx3 Sx2][a]   [Sx2y]
        # [Sx3 Sx2 Sx ][b] = [Sxy ]
        # [Sx2 Sx  n  ][c]   [Sy  ]
        import itertools
        A = [[Sx4,Sx3,Sx2],[Sx3,Sx2,Sx],[Sx2,Sx,n]]
        B = [Sx2y,Sxy,Sy]
        # Gaussian elimination
        M = [row[:] + [b] for row,b in zip(A,B)]
        for i in range(3):
            piv = max(range(i,3), key=lambda r: abs(M[r][i]))
            M[i],M[piv] = M[piv],M[i]
            if abs(M[i][i]) < 1e-12:
                return (0,0,sum(ys)/n)
            for r in range(i+1,3):
                f = M[r][i]/M[i][i]
                for c in range(i,4):
                    M[r][c] -= f*M[i][c]
        sol = [0,0,0]
        for i in range(2,-1,-1):
            s = M[i][3] - sum(M[i][j]*sol[j] for j in range(i+1,3))
            sol[i] = s/M[i][i]
        return tuple(sol)

    # Left side data (x <= -20.3)
    left_x = [-120,-100,-80,-60,-50.4,-40,-30,-24.3,-20.3]
    left_y = [22280.0824,15882.924,9582.0843,4736.4186,2995.4039,1531.8654,548.2541,166.2134,-15.8672]
    la, lb, lc = quad_fit(left_x, left_y)

    # Right side data (x >= 5)
    right_x = [5,10,20,21.3,30,40,60,66.0,72.7,80,88.2,100]
    right_y = [48.3879,650.4807,1914.2369,2091.9289,3458.112,5505.5302,10959.9624,12950.8364,15366.0691,18320.3968,21854.2087,26939.4501]
    ra, rb, rc = quad_fit(right_x, right_y)

    FLAT = -20.4469
    # Boundaries: left boundary between -20.3 and -20; right boundary between 2.9 and 5.
    # Use -20.15 and 3.95 as midpoints (guess).
    LEFT_B = -20.15
    RIGHT_B = 3.95

    out = []
    for x in probe.get("x", []):
        if x <= LEFT_B:
            y = la*x*x + lb*x + lc
        elif x >= RIGHT_B:
            y = ra*x*x + rb*x + rc
        else:
            y = FLAT
        out.append(y)
    return {"y": out}

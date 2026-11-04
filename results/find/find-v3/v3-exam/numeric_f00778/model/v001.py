def predict(probe):
    # Looks like a cubic: y = a*x^3 + b*x^2 + c*x + d [E1]
    # Fit from E1 data. Check: x=2.9 -> -87.69, x=-6 -> 825.5
    # Try pure cubic-ish. Let's fit coefficients.
    import math
    xs = probe["x"]
    # Fit a cubic through E1 points using least squares mentally? 
    # Use known: try y = x^3 * k. For x=88.2: 88.2^3=686128, y=-2677279 -> k=-3.902
    # x=66: 287496, y=-1121969 -> k=-3.902. x=-20.3: -8365, y=32503 -> k=-3.886
    # x=-61.7: -234885, y=915168 -> k=-3.896. x=2.9: 24.389, y=-87.69 -> k=-3.595
    # x=-24.3: -14349, y=55795 -> k=-3.888. x=72.7: 384240, y=-1499448 -> k=-3.902
    # x=-50.4: -128024, y=498688 -> k=-3.895. x=-6: -216, y=825.5 -> k=-3.822
    # x=21.3: 9663, y=-37734 -> k=-3.905
    # Looks like y = -3.9 * x^3 roughly, but small x deviates (2.9, -6)
    # Maybe y = -3.9*x^3 + something. At x=2.9: -3.9*24.389=-95.1, actual -87.69, diff +7.4
    # At x=-6: -3.9*-216=842.4, actual 825.5, diff -16.9
    # Hmm. Try y = a*x^3 + b*x. 
    # From x=88.2 and x=66: 
    # a*686128 + b*88.2 = -2677279
    # a*287496 + b*66 = -1121969
    # Solve: from second b = (-1121969 - 287496a)/66
    # Sub: a*686128 + 88.2*(-1121969-287496a)/66 = -2677279
    # 686128a - 1.33636*(1121969+287496a) = -2677279
    # 686128a - 1499450 - 384177a = -2677279
    # 301951a = -1177829 -> a = -3.9007
    # b = (-1121969 - 287496*(-3.9007))/66 = (-1121969+1121278)/66 = -691/66 = -10.47
    # Check x=2.9: -3.9007*24.389 -10.47*2.9 = -95.13 -30.36 = -125.5, actual -87.69. No.
    # Try y = a*x^3 + c*x + d
    # Use x=2.9, -6, 21.3 to solve
    # 24.389a + 2.9c + d = -87.6888
    # -216a -6c + d = 825.4999
    # 9663.6a + 21.3c + d = -37734.5152
    # Subtract eq1 from eq2: -240.389a -8.9c = 913.1887
    # Subtract eq1 from eq3: 9639.2a + 18.4c = -37646.826
    # From first: c = (-240.389a - 913.1887)/8.9 = -27.01a - 102.6
    # Sub: 9639.2a + 18.4*(-27.01a -102.6) = -37646.8
    # 9639.2a - 497.0a - 1887.8 = -37646.8
    # 9142.2a = -35759 -> a = -3.9114
    # c = -27.01*(-3.9114) -102.6 = 105.65 -102.6 = 3.05
    # d = -87.6888 - 24.389*(-3.9114) - 2.9*3.05 = -87.6888 +95.39 -8.845 = -1.14
    # Check x=88.2: -3.9114*686128 + 3.05*88.2 -1.14 = -2683738 +269 -1 = -2683470, actual -2677279. Off by 6191.
    # Not quite. Maybe there's a quartic or the coefficient isn't constant.
    # Let's just do a cubic fit through 4 points properly.
    # Use x=88.2, 66, -61.7, 72.7 (large values dominate)
    # Actually let me just do least squares cubic in code.
    xs_data = [88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3]
    ys_data = [-2677279.3383,-1121968.9588,32503.8673,915168.6653,-87.6888,55795.6757,-1499448.4879,498688.5544,825.4999,-37734.5152]
    # Normal equations for cubic y = a x^3 + b x^2 + c x + d
    import itertools
    n = len(xs_data)
    # build matrix
    A = [[0.0]*4 for _ in range(4)]
    B = [0.0]*4
    for x,y in zip(xs_data,ys_data):
        p = [x**3, x**2, x, 1.0]
        for i in range(4):
            B[i] += p[i]*y
            for j in range(4):
                A[i][j] += p[i]*p[j]
    # gaussian elimination
    for i in range(4):
        piv = A[i][i]
        for j in range(i+1,4):
            f = A[j][i]/piv
            for k in range(4):
                A[j][k] -= f*A[i][k]
            B[j] -= f*B[i]
    coef = [0.0]*4
    for i in range(3,-1,-1):
        s = B[i]
        for j in range(i+1,4):
            s -= A[i][j]*coef[j]
        coef[i] = s/A[i][i]
    a,b,c,d = coef
    out = []
    for x in xs:
        out.append(a*x**3 + b*x**2 + c*x + d)
    return {"y": out}

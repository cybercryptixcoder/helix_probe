def predict(probe):
    # f is flat at -84.3663 for |x| <= ~50, not 32 [E6, E7, E8]
    #   E6: all of -50..-20 and 20..26 flat; E7: -32..26 flat
    #   E8: -50..-40 flat, but -52 = 1853.9, -56 = 12306.9, -64 = 44756.7
    # So the flat region extends to about |x| = 51 on the negative side.
    # Positive side: E8 shows 40..48 flat too; E1 shows f(64)=15971, so
    #   boundary is between 48 and 64 on positive side too. [?]
    # Outside, f grows smoothly and is NOT symmetric: negative side larger [E1,E2]
    # Positive: f(64)=15971, f(72)=42011, f(80)=72734, f(96)=134517,
    #   f(100)=149963, f(112)=196300, f(120)=227192, f(128)=258083 [E1,E2]
    # Negative: f(-64)=44756, f(-72)=79980, f(-80)=115204, f(-96)=185653,
    #   f(-100)=203265, f(-104)=220877, f(-112)=256101, f(-120)=291325,
    #   f(-128)=326549 [E1,E2]
    # Fit quadratic in (|x| - 51) separately per sign using outer points. [?]
    import math
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ax = abs(x)
            if ax <= 51:
                y = -84.3663
            else:
                d = ax - 51.0
                if x > 0:
                    # points (d,y): (13,15971),(21,42011),(29,72734),(45,134517),
                    # (49,149963),(61,196300),(69,227192),(77,258083)
                    # least-squares quadratic y = a d^2 + b d + c
                    pts = [(13,15971),(21,42011),(29,72734),(45,134517),
                           (49,149963),(61,196300),(69,227192),(77,258083)]
                else:
                    pts = [(13,44756),(21,79980),(29,115204),(45,185653),
                           (49,203265),(53,220877),(61,256101),(69,291325),
                           (77,326549)]
                # solve normal equations for quadratic
                S = [sum(d**k for d,_ in pts) for k in range(5)]
                T = [sum((d**k)*y for d,y in pts) for k in range(3)]
                # S0..S4, T0..T2
                # [S0 S1 S2][c]   [T0]
                # [S1 S2 S3][b] = [T1]
                # [S2 S3 S4][a]   [T2]
                M = [[S[0],S[1],S[2]],[S[1],S[2],S[3]],[S[2],S[3],S[4]]]
                V = [T[0],T[1],T[2]]
                # gaussian elimination
                for i in range(3):
                    p = M[i][i]
                    for j in range(i+1,3):
                        f = M[j][i]/p
                        for k in range(i,3):
                            M[j][k] -= f*M[i][k]
                        V[j] -= f*V[i]
                sol = [0,0,0]
                for i in range(2,-1,-1):
                    s = V[i]
                    for k in range(i+1,3):
                        s -= M[i][k]*sol[k]
                    sol[i] = s/M[i][i]
                c,b,a = sol
                y = a*d*d + b*d + c
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}

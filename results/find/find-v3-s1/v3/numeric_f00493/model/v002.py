import math

def predict(probe):
    # Model of f(x):
    # - For 0 < x < 1: f = 0 [E4, E8]
    # - For x >= 1: f is negative, magnitude grows like a power law.
    # - For -1 < x < 0: f is positive, small (~4-6.4), roughly linear in |x| [E8, E10]
    # - For x <= -1: f is negative for x < -1 (except boundary x=-1 -> +6.1),
    #   with a jump just past -1 then decreasing [E10].
    # - The magnitude law is NOT a single power law; log-log slope grows with x.
    #   Fit log|f| as quadratic in log|x| separately for positive and negative sides.
    # - Positive side: f(1)=-4.3, f(2)=-60.2, f(3)=-427.5, f(10)=-442789,
    #   f(100)=-4.91e11 [E2]. Negative side magnitudes slightly larger [E12,E14].
    # - Sign: f<0 for x>0 (x>=1), f>0 for -1<x<0, f<0 for x<-1, f(-1)=+6.1.

    # Fit positive side: log|f| = a + b*u + c*u^2, u=log(t), t=|x|>=1
    # Points (t, |f|): (1,4.3),(2,60.2),(3,427.5),(10,442789),(100,4.91e11)
    # Also E6/E4 give many intermediate points; use a robust fit.
    # Let's fit using least squares on log-log with quadratic.
    pos_pts = [
        (1.0, 4.3), (1.1, 5.2257), (1.2, 6.4027), (1.3, 7.8647), (1.4, 9.6501),
        (1.5, 11.8031), (1.6, 14.3742), (1.7, 17.4207), (1.8, 21.0072), (1.9, 25.2065),
        (2.0, 60.2), (2.1, 71.5566), (2.2, 84.6838), (2.4, 117.1594), (2.5, 137.0188),
        (2.6, 159.6733), (2.8, 214.664), (3.0, 427.5), (3.1, 490.4189), (3.2, 561.0274),
        (3.4, 728.3438), (3.5, 826.6969), (3.6, 936.0331), (3.8, 1191.5544), (4.0, 2004.4),
        (4.2, 2507.5373), (4.5, 3457.0875), (5.5, 11271.6406), (6.0, 20683.8),
        (6.5, 30683.0062), (7.0, 51702.7), (7.5, 72935.0344), (8.0, 115148.0),
        (8.5, 156124.775), (9.0, 234189.9), (10.0, 442789.0), (12.0, 1336525.2),
        (100.0, 4.91e11),
    ]
    # least squares for a + b*u + c*u^2
    n = len(pos_pts)
    Su = Sv = Suu = Suuu = Suuuu = Suv = Suuv = 0.0
    for t, m in pos_pts:
        u = math.log(t); v = math.log(m)
        Su += u; Sv += v; Suu += u*u; Suuu += u**3; Suuuu += u**4
        Suv += u*v; Suuv += u*u*v
    # normal equations
    # [n Su Suu][a]   [Sv]
    # [Su Suu Suuu][b] = [Suv]
    # [Suu Suuu Suuuu][c]  [Suuv]
    A = [[n, Su, Suu], [Su, Suu, Suuu], [Suu, Suuu, Suuuu]]
    B = [Sv, Suv, Suuv]
    # solve 3x3
    def solve3(A, B):
        M = [row[:] + [B[i]] for i, row in enumerate(A)]
        for i in range(3):
            p = max(range(i, 3), key=lambda r: abs(M[r][i]))
            M[i], M[p] = M[p], M[i]
            if abs(M[i][i]) < 1e-15:
                return [0, 0, 0]
            for r in range(3):
                if r != i:
                    f = M[r][i] / M[i][i]
                    for cc in range(i, 4):
                        M[r][cc] -= f * M[i][cc]
        return [M[i][3] / M[i][i] for i in range(3)]
    pa, pb, pc = solve3(A, B)

    # Negative side magnitudes: from E12, E14, E2, E10
    neg_pts = [
        (1.0, 6.1), (1.01, 12.0665), (1.02, 11.9258), (1.05, 11.4595), (1.1, 10.5259),
        (1.3, 4.4607), (1.5, 6.4313), (2.0, 67.0), (2.5, 310.5656), (3.0, 722.7),
        (4.0, 3534.8), (5.0, 12155.5), (6.0, 33683.4), (8.0, 171815.2),
        (10.0, 618311.0), (12.0, 1776726.0), (15.0, 6527191.5), (20.0, 35356522.0),
        (25.0, 132033027.5), (30.0, 388817433.0), (40.0, 2147947844.0),
        (45.0, 4330460299.5), (60.0, 24067524366.0), (70.0, 60410784077.0),
        (90.0, 271236660399.0), (100.0, 5.093e11), (110.0, 900725977921.0),
        (125.0, 1935566921387.5),
    ]
    n2 = len(neg_pts)
    Su = Sv = Suu = Suuu = Suuuu = Suv = Suuv = 0.0
    for t, m in neg_pts:
        u = math.log(t); v = math.log(m)
        Su += u; Sv += v; Suu += u*u; Suuu += u**3; Suuuu += u**4
        Suv += u*v; Suuv += u*u*v
    A2 = [[n2, Su, Suu], [Su, Suu, Suuu], [Suu, Suuu, Suuuu]]
    B2 = [Sv, Suv, Suuv]
    na, nb, nc = solve3(A2, B2)

    def g_pos(t):
        u = math.log(t)
        return math.exp(pa + pb*u + pc*u*u)

    def g_neg(t):
        u = math.log(t)
        return math.exp(na + nb*u + nc*u*u)

    def g_small_neg(t):
        # 0<t<1, x=-t, positive value ~ 4.1 + 4.2*t
        return 4.1 + 4.2*t

    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None); continue
        try:
            if x > 1.0:
                out.append(-g_pos(x))
            elif x == 1.0:
                out.append(-4.3)
            elif 0 < x < 1.0:
                out.append(-0.0)
            elif x == 0.0:
                out.append(-0.0)
            elif -1.0 < x < 0:
                out.append(g_small_neg(-x))
            elif x == -1.0:
                out.append(6.1)
            else:  # x < -1
                out.append(-g_neg(-x))
        except Exception:
            out.append(None)
    return {"y": out}

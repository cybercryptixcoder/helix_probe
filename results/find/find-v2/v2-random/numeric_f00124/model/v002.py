def predict(probe):
    # f(x) is a smooth MLP approximating a function that is roughly quadratic
    # for large |x| but has a bump/plateau structure at small-to-moderate x.
    # Evidence: E1 and E2 both show y ~ 0.9*x^2 + small linear term for large x,
    # but small x values deviate (e.g. x=2.9 -> 429, x=1.2 -> 240, x=-6 -> 131).
    # A single quadratic fit fails at small x (E2 match 0.30).
    # Model: y = a*x^2 + b*x + c + d*exp(-(x-mu)^2/(2*s^2))  (Gaussian bump)
    # Fit to all 20 points from E1 and E2.
    import math
    xs = [88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3,
          104.5,1.2,-55.8,65.5,30.3,-63.9,104.9,123.6,79.4,103.0]
    ys = [9933.9859,7460.2885,503.8102,1583.1784,429.1934,608.097,8206.8548,1288.5682,130.985,2479.4652,
          11750.2593,239.7661,1429.3554,7404.5746,3482.3155,1640.5361,11794.8304,13878.5306,8953.4212,11583.1176]
    # Grid search over bump center and width, linear least squares for a,b,c,d
    best = None
    for mu in [x/2.0 for x in range(-40, 41)]:
        for s in [1,2,3,4,5,6,8,10,12,15,20,25,30]:
            # basis: x^2, x, 1, exp(-(x-mu)^2/(2s^2))
            B = []
            for x in xs:
                g = math.exp(-((x-mu)**2)/(2*s*s))
                B.append([x*x, x, 1.0, g])
            # normal equations 4x4
            A = [[sum(B[i][r]*B[i][c] for i in range(len(xs))) for c in range(4)] for r in range(4)]
            T = [sum(ys[i]*B[i][r] for i in range(len(xs))) for r in range(4)]
            # solve
            M = [row[:] + [T[r]] for r, row in enumerate(A)]
            ok = True
            for i in range(4):
                p = M[i][i]
                if abs(p) < 1e-12:
                    ok = False; break
                for j in range(i+1, 4):
                    f = M[j][i]/p
                    for k in range(i, 5):
                        M[j][k] -= f*M[i][k]
            if not ok: continue
            coef = [0]*4
            for i in range(3, -1, -1):
                coef[i] = (M[i][4] - sum(M[i][k]*coef[k] for k in range(i+1,4)))/M[i][i]
            # residual
            err = 0
            for i in range(len(xs)):
                pred = sum(coef[r]*B[i][r] for r in range(4))
                err += (pred-ys[i])**2
            if best is None or err < best[0]:
                best = (err, mu, s, coef)
    err, mu, s, coef = best
    a,b,c,d = coef
    def f(x):
        return a*x*x + b*x + c + d*math.exp(-((x-mu)**2)/(2*s*s))
    return {"y":[f(x) for x in probe["x"]]}

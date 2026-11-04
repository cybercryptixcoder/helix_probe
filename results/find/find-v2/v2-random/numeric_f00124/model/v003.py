def predict(probe):
    # f is a smooth MLP approximating a function that is nearly quadratic for large |x|.
    # E1/E2/E3 all fit y ≈ a*x^2 + b*x + c well at large |x| (a≈0.9).
    # Small-to-moderate x deviates from pure quadratic: there is a bump/plateau region.
    # E3 shows the Gaussian-bump model (v2) is close but slightly off in the mid region:
    #   x=-48.6 pred 1366 vs obs 1242; x=-102.2 pred 2119 vs obs 2639; x=-16.9 pred 277 vs obs 415.
    # The bump appears centered near small positive x and affects negative-mid region too.
    # Refit a quadratic + Gaussian bump using ALL evidence (E1,E2,E3) via grid search.
    import math
    xs = [88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3,
          104.5,1.2,-55.8,65.5,30.3,-63.9,104.9,123.6,79.4,103.0,
          -48.6,58.8,102.1,47.1,-7.1,-102.2,-16.9,28.4,105.7,119.5]
    ys = [9933.9859,7460.2885,503.8102,1583.1784,429.1934,608.097,8206.8548,1288.5682,130.985,2479.4652,
          11750.2593,239.7661,1429.3554,7404.5746,3482.3155,1640.5361,11794.8304,13878.5306,8953.4212,11583.1176,
          1241.6392,6658.0082,11482.8326,5354.3028,159.6639,2639.082,415.1665,3270.6027,11883.9727,13421.6765]
    best = None
    for mu in [x/2.0 for x in range(-40, 41)]:
        for s in [1,2,3,4,5,6,8,10,12,15,20,25,30]:
            B = []
            for x in xs:
                g = math.exp(-((x-mu)**2)/(2*s*s))
                B.append([x*x, x, 1.0, g])
            A = [[sum(B[i][r]*B[i][c] for i in range(len(xs))) for c in range(4)] for r in range(4)]
            T = [sum(ys[i]*B[i][r] for i in range(len(xs))) for r in range(4)]
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

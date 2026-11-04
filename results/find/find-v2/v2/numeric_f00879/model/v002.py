import math

def predict(probe):
    # Beliefs:
    # - Output is not a single sinusoid; it's noisy/irregular [E1, E2, E3].
    # - E2 shows large-scale structure: values swing between ~-1.8 and ~1.8
    #   across x in [-128,128], with no clean period visible [E2].
    # - E3 shows y up to 3.6 at x~104.5, and 2.16 at x~1.2 — amplitude varies
    #   with x, so a constant-amplitude sinusoid is wrong [E3].
    # - E1 and E3 both show high values near x~70-105 and low near x~-20 to -60.
    # - Hypothesis: y = sin(x) + sin(x/3) + sin(x/7) type multi-frequency sum,
    #   plus noise. Try a small sum of sinusoids fit to all data.
    #
    # Data collected:
    xs = [88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3,
          -128,-100,-80,-40,-30,-10,0,10,30,40,50,60,80,100,120,128,
          104.5,1.2,-55.8,65.5,30.3,-63.9,104.9,123.6,79.4,103.0]
    ys = [1.1293,0.1485,-1.9104,1.2025,1.4833,-0.1702,2.2951,-0.3553,-0.9291,0.5647,
          -0.4324,-0.1357,-1.8255,0.1285,-0.0364,-1.1977,0.0397,1.7667,0.6774,-0.0742,
          1.0516,0.2142,0.2507,-0.4998,1.1881,1.1879,
          3.6456,2.1599,-1.3044,0.2742,-0.3413,-0.8627,1.3933,0.071,1.7589,0.5872]

    # Fit y = sum_k [a_k sin(w_k x) + b_k cos(w_k x)] + c
    # Use a set of frequencies and least squares.
    freqs = [0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]
    # Build design matrix
    n = len(xs)
    cols = []
    for w in freqs:
        cols.append([math.sin(w*x) for x in xs])
        cols.append([math.cos(w*x) for x in xs])
    cols.append([1.0]*n)
    p = len(cols)

    # Normal equations A^T A coef = A^T y
    ATA = [[0.0]*p for _ in range(p)]
    ATy = [0.0]*p
    for i in range(p):
        for j in range(p):
            s = 0.0
            ci = cols[i]; cj = cols[j]
            for k in range(n):
                s += ci[k]*cj[k]
            ATA[i][j] = s
        s = 0.0
        ci = cols[i]
        for k in range(n):
            s += ci[k]*ys[k]
        ATy[i] = s

    # Solve with Gaussian elimination + small ridge for stability
    for i in range(p):
        ATA[i][i] += 1e-6
    M = [row[:] + [ATy[i]] for i, row in enumerate(ATA)]
    for i in range(p):
        piv = max(range(i, p), key=lambda r: abs(M[r][i]))
        if abs(M[piv][i]) < 1e-12:
            continue
        M[i], M[piv] = M[piv], M[i]
        pv = M[i][i]
        for j in range(i, p+1):
            M[i][j] /= pv
        for r in range(p):
            if r != i:
                f = M[r][i]
                if f != 0.0:
                    for j in range(i, p+1):
                        M[r][j] -= f*M[i][j]
    coef = [M[i][p] for i in range(p)]

    def f(x):
        s = 0.0
        idx = 0
        for w in freqs:
            s += coef[idx]*math.sin(w*x) + coef[idx+1]*math.cos(w*x)
            idx += 2
        s += coef[idx]
        return s

    return {"y":[f(x) for x in probe["x"]]}

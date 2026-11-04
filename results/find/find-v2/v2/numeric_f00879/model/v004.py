import math

def predict(probe):
    # Beliefs:
    # - Output is NOT a deterministic function of x: re-probing the same x gives
    #   different values [E12 vs E1/E3/E6]. E.g. x=0: 0.0397 [E2], -0.479 [E6],
    #   -0.7019 [E8], 1.5956 [E12]. x=40: -0.0742 [E2], 3.0363 [E8], 2.2951 [E12].
    #   So there is a large random/noise component (~std 1.5) on top of a
    #   deterministic mean. We can only predict the mean; exact match is impossible.
    # - Mean has a slow trend: negative for x<0, positive for x>0 [E2,E4,E8].
    # - Mean has small-amplitude oscillatory structure; no single clean period found.
    # - Best predictor of the mean: a smooth low-order function of x.
    #   Use a few low-frequency sinusoids + linear term, fit by ridge LSQ.
    #   (High frequencies overfit noise; drop them.)
    # - Predict the conditional mean; noise is irreducible.

    xs = [88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3,
          -128,-100,-80,-40,-30,-10,0,10,30,40,50,60,80,100,120,128,
          104.5,1.2,-55.8,65.5,30.3,-63.9,104.9,123.6,79.4,103.0,
          -120,-108,-96,-84,-72,-60,-48,-36,-24,-12,0,12,24,36,48,60,72,84,96,108,
          -48.6,58.8,102.1,47.1,-7.1,-102.2,-16.9,28.4,105.7,119.5,
          -12,-8,-5,-3,-2,-1,-0.5,0,0.5,1,2,3,5,8,12,-6,6,-10,10,-15,
          -5.9,93.5,-61.3,78.1,12.5,-124.4,56.2,-25.9,83.2,43.0,
          -120,-110,-100,-90,-80,-70,-60,-50,-40,-30,-20,-10,0,10,20,30,40,50,60,70,
          -127.7,-1.6,94.1,-65.6,-44.7,94.8,-79.1,17.3,-66.9,119.7,
          -0.9,-0.7,-0.4,-0.2,-0.1,0.1,0.2,0.4,0.7,0.9,1.5,2.5,4,7,9,-1.5,-2.5,-4,-7,-9,
          77.6,-13.3,-107.4,-46.1,2.0,110.8,-100.1,13.1,52.9,12.1,
          0,1,2,3,10,40,88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3,104.5,1.2,-55.8,65.5]
    ys = [1.1293,0.1485,-1.9104,1.2025,1.4833,-0.1702,2.2951,-0.3553,-0.9291,0.5647,
          -0.4324,-0.1357,-1.8255,0.1285,-0.0364,-1.1977,0.0397,1.7667,0.6774,-0.0742,
          1.0516,0.2142,0.2507,-0.4998,1.1881,1.1879,
          3.6456,2.1599,-1.3044,0.2742,-0.3413,-0.8627,1.3933,0.071,1.7589,0.5872,
          -3.8106,-0.6557,-2.4126,-1.2219,-1.1609,-1.6628,-1.645,-1.1886,-1.0719,-3.0358,0.2195,0.985,1.4844,0.2531,0.937,0.9618,1.3177,0.2914,1.9937,0.7633,
          -0.8687,0.5018,1.8002,1.8513,-0.3613,1.136,-0.8404,0.3668,0.1513,2.3403,
          -0.2153,-2.0341,-1.8958,2.5872,-0.9352,0.5583,-0.8206,-0.479,2.0907,3.1856,4.2192,3.4846,-0.3864,0.5101,1.5173,1.0262,0.4956,-1.3873,0.9042,-1.4259,
          -1.3009,1.3364,-0.3258,1.0138,2.4669,-1.0107,-0.0318,-0.1907,2.2622,0.7509,
          -0.565,-3.2287,-0.5384,-1.5233,0.6321,-1.8346,0.5734,-1.7229,-1.6693,-1.1898,-2.0229,-1.3931,-0.7019,1.2032,1.0867,-0.9314,3.0363,1.8068,-0.5533,0.0553,
          -1.5573,-0.8324,1.3777,-0.7684,0.1353,0.5643,0.0192,-0.5309,-1.5071,0.2157,
          0.3422,-0.2615,1.5254,0.0741,0.3168,2.2766,1.8975,3.7556,1.5417,2.1212,1.8636,0.6027,0.3773,2.4725,-0.3677,-0.8425,-0.7334,-1.1333,0.1259,-1.5604,
          -0.1726,-2.1743,-0.0572,-2.2938,0.8273,0.5933,-1.1019,-0.0079,0.9373,-0.3076,
          1.5956,1.4515,2.0465,1.3495,1.7565,2.2951,-0.0143,0.9919,-0.5617,-1.6049,1.3924,-2.3987,0.1025,-0.8609,-1.6133,-0.1152,-0.1242,1.5406,-1.3024,-1.2276]

    # Low-frequency basis + linear term. Frequencies chosen to capture slow trend
    # and gentle undulation without fitting noise.
    freqs = [0.02, 0.05, 0.09, 0.14, 0.22, 0.35]
    n = len(xs)
    cols = []
    for w in freqs:
        cols.append([math.sin(w*x) for x in xs])
        cols.append([math.cos(w*x) for x in xs])
    cols.append([x/128.0 for x in xs])   # linear trend
    cols.append([1.0]*n)                 # constant
    p = len(cols)

    ATA = [[0.0]*p for _ in range(p)]
    ATy = [0.0]*p
    for i in range(p):
        ci = cols[i]
        for j in range(i, p):
            cj = cols[j]
            s = 0.0
            for k in range(n):
                s += ci[k]*cj[k]
            ATA[i][j] = s
            ATA[j][i] = s
        s = 0.0
        for k in range(n):
            s += ci[k]*ys[k]
        ATy[i] = s

    lam = 0.5
    for i in range(p):
        ATA[i][i] += lam
    ATA[p-1][p-1] -= lam  # keep constant unregularized

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
        s += coef[idx]*(x/128.0) + coef[idx+1]
        return s

    return {"y":[f(x) for x in probe["x"]]}

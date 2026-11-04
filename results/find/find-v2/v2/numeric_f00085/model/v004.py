import math

def predict(probe):
    # Mechanism hypothesis (v4), from all evidence:
    # A: There is a flat plateau at exactly -22.8021 for x in [NEG_EDGE, POS_EDGE].
    #    E10 pins edges tightly: -7.4 -> -19.3504 (off), -7.2 -> -22.8021 (on).
    #    So NEG_EDGE is between -7.4 and -7.2, use -7.3.
    #    Positive: 5.8 -> -22.6269 (barely off), 5.6 -> -22.8021 (on).
    #    So POS_EDGE between 5.6 and 5.8, use 5.7. [E4,E6,E10]
    # B: Outside the plateau, y is a smooth curve. The transition is SHARP and steep:
    #    E10 negative: -7.4->-19.35, -7.6->-6.64, -7.9->12.42, -8.2->46.59, -8.6->96.13, -9.0->145.67
    #    E10 positive: 5.8->-22.63, 6.0->-8.55, 6.2->5.52, 6.4->19.60, 6.6->33.67, 6.8->47.74,
    #                  7.0->61.82, 7.4->89.97, 7.8->118.12
    #    The positive side near transition is nearly LINEAR in x with slope ~70/unit:
    #      from 6.0 to 7.8: (118.12-(-8.55))/1.8 = 70.4. Very linear!
    #    Negative side near transition also nearly linear: from -7.4 to -9.0:
    #      (145.67-(-19.35))/1.6 = 103.1 slope (steeper).
    # C: Far out, y ~ quadratic but saturating (MLP tanh). Ratio y/x^2 ~3.5 mid, ~3.14 at 124.
    #    Asymmetry: y(-x)-y(x) ~ 7.7*|x| for |x|>=12 -> linear term b~-3.8 in y=a x^2+b x+c.
    #    But pure quadratic fails mid-range. Best: piecewise cubic fit per side using ALL data,
    #    which captures both the steep transition and the far saturation.
    # D: The transition region is steep and roughly linear; a global cubic per side
    #    under-fits it badly (v3 gave ~200 at x=6). Need a dedicated transition model.
    #    Approach: fit a cubic to the FULL positive data (including transition points) and
    #    FULL negative data. The transition points are dense enough to anchor the cubic.
    #    But cubic can't capture both steep-linear near edge AND quadratic far out well.
    #    Better: use a piecewise model with a transition segment (linear-ish) and a
    #    far segment (quadratic-ish), blended. Let me instead fit a quartic per side
    #    to all points, which has more freedom to match the steep rise and far curve.

    # Full positive data (x,y):
    pos = [(5.8,-22.6269),(6.0,-8.5526),(6.1,-1.5154),(6.2,5.5217),(6.3,12.5589),
           (6.4,19.596),(6.6,33.6703),(6.7,40.7075),(6.8,47.7447),(7.0,61.819),
           (7.2,75.8933),(7.4,89.9676),(7.5,97.0047),(7.7,111.079),(7.8,118.1162),
           (8.0,132.1905),(8.2,146.2648),(8.5,167.3763),(8.7,181.4506),(9.0,202.5621),
           (9.2,216.6364),(9.5,237.7478),(9.7,251.8221),(10.0,272.9336),(10.2,287.0079),
           (10.5,308.1194),(11.0,343.3051),(11.5,378.4909),(12.0,421.8308),(12.5,476.233),
           (13.0,530.6351),(15.0,748.2438),(20.0,1357.3016),(21.3,1532.7222),
           (25.0,2094.9201),(28.4,2728.3058),(30.0,3042.9824),(30.3,3107.5411),
           (40.0,5460.3248),(43.0,6322.2252),(47.1,7600.659),(50.0,8572.4127),
           (56.2,10856.0129),(58.8,11895.2568),(60.0,12387.5033),(65.5,14783.3988),
           (66.0,15014.0187),(70.0,16904.4711),(72.7,18241.8226),(78.1,21126.746),
           (79.4,21894.3945),(83.2,24138.29),(88.2,27090.784),(90.0,28153.6819),
           (93.5,30220.4277),(94.1,30574.727),(94.8,30988.0762),(102.1,35298.7175),
           (103.0,35830.1665),(104.5,36715.9147),(104.9,36952.1142),(105.7,37424.5133),
           (110.0,39963.6581),(119.5,45573.3969),(119.7,45691.4966),(120.0,45868.6463),
           (123.6,47994.442),(125.0,48821.1403)]
    # Full negative data (x,y):
    neg = [(-7.4,-19.3504),(-7.5,-12.9955),(-7.6,-6.6407),(-7.8,6.069),(-7.9,12.4239),
           (-8.0,21.8213),(-8.2,46.592),(-8.5,83.748),(-8.6,96.1333),(-9.0,145.6747),
           (-9.5,207.6015),(-10.0,269.5282),(-12.0,517.2351),(-15.0,888.7955),
           (-16.9,1124.117),(-20.0,1508.0627),(-20.3,1545.2188),(-24.3,2154.0941),
           (-25.0,2277.7612),(-25.9,2436.7616),(-30.0,3259.3629),(-44.7,7158.2693),
           (-48.6,8447.0973),(-50.0,8934.3388),(-50.4,9077.3007),(-55.8,11101.3559),
           (-60.0,12818.1115),(-61.3,13377.8579),(-61.7,13550.6196),(-63.9,14524.3579),
           (-65.6,15303.2482),(-66.9,15909.6219),(-70.0,17406.7659),(-79.1,22354.7983),
           (-90.0,28789.5493),(-102.2,35991.7477),(-110.0,40596.4319),(-120.0,46499.8732),
           (-124.4,49097.3874),(-125.0,49451.5938),(-127.7,51045.523)]

    def lsq_poly(pts, deg):
        n = len(pts)
        m = deg+1
        S = [[0.0]*m for _ in range(m)]
        T = [0.0]*m
        for x,y in pts:
            pw = [1.0]
            for k in range(1, 2*deg+1):
                pw.append(pw[-1]*x)
            for i in range(m):
                for j in range(m):
                    S[i][j] += pw[i+j]
                T[i] += pw[i]*y
        A = [row[:] + [T[i]] for i,row in enumerate(S)]
        for col in range(m):
            piv = max(range(col,m), key=lambda r: abs(A[r][col]))
            if abs(A[piv][col]) < 1e-12:
                continue
            A[col],A[piv] = A[piv],A[col]
            pv = A[col][col]
            for j in range(col,m+1):
                A[col][j] /= pv
            for r in range(m):
                if r!=col and abs(A[r][col])>1e-15:
                    f = A[r][col]
                    for j in range(col,m+1):
                        A[r][j] -= f*A[col][j]
        return [A[i][m] for i in range(m)]

    # Quartic fits per side (more freedom to capture steep transition + far curve)
    pc = lsq_poly(pos, 4)
    nc = lsq_poly(neg, 4)

    PLATEAU = -22.8021
    POS_EDGE = 5.7    # between 5.6 (on) and 5.8 (off) [E10]
    NEG_EDGE = -7.3   # between -7.4 (off) and -7.2 (on) [E10]

    def evalpoly(coef, x):
        r = 0.0
        for c in reversed(coef):
            r = r*x + c
        return r

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if x is None:
                ys.append(None); continue
            x = float(x)
            if NEG_EDGE <= x <= POS_EDGE:
                ys.append(PLATEAU)
            elif x > POS_EDGE:
                ys.append(evalpoly(pc, x))
            else:
                ys.append(evalpoly(nc, x))
        except Exception:
            ys.append(None)
    return {"y": ys}

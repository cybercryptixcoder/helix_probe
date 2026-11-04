import math

def predict(probe):
    # Mechanism hypothesis (v5), from all evidence:
    # A: Flat plateau at exactly -22.8021 for x in [NEG_EDGE, POS_EDGE].
    #    E12 pins edges tightly:
    #      negative: -7.4 -> -19.3504 (off), -7.35 -> -22.5278 (off), -7.3 -> -22.8021 (on)
    #      positive: 5.75 -> -22.8021 (on), 5.8 -> -22.6269 (off)
    #    So NEG_EDGE in (-7.35,-7.3], POS_EDGE in [5.75,5.8). Use -7.32 and 5.78.
    # B: Transition is SMOOTH (tanh-like), not a sharp step. E12 dense points:
    #    negative side: -7.5->-12.9955, -7.4->-19.3504, -7.35->-22.5278, then plateau.
    #    positive side: 5.8->-22.6269, 5.85->-19.1083, 5.9->-15.5897, 5.95->-12.0712,
    #                   6.0->-8.5526, 6.05->-5.034, 6.1->-1.5154.
    #    Positive transition is nearly LINEAR with slope ~70/unit (from E10: 6.0..7.8 slope 70.4).
    #    Negative transition is steeper near edge then curves.
    # C: Far out, y ~ quadratic with slight saturation (MLP tanh). Asymmetry:
    #    y(-x)-y(x) ~ +7.7*|x| for large |x| (E8 confirms linear asymmetry throughout).
    # D: Model: plateau, then a smooth blend from plateau value into a per-side
    #    polynomial (quartic fit to full data), using a tanh blend over a transition
    #    width so the steep near-edge rise is captured without a hard step.
    #    The quartic alone under-fits the steep transition; the blend fixes it.

    pos = [(5.8,-22.6269),(5.85,-19.1083),(5.9,-15.5897),(5.95,-12.0712),(6.0,-8.5526),
           (6.05,-5.034),(6.1,-1.5154),(6.2,5.5217),(6.3,12.5589),
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
    neg = [(-7.5,-12.9955),(-7.4,-19.3504),(-7.35,-22.5278),
           (-7.6,-6.6407),(-7.8,6.069),(-7.9,12.4239),
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

    pc = lsq_poly(pos, 4)
    nc = lsq_poly(neg, 4)

    PLATEAU = -22.8021
    POS_EDGE = 5.78
    NEG_EDGE = -7.32
    # transition half-widths for tanh blend
    POS_W = 0.35
    NEG_W = 0.30

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
                # blend from plateau into positive quartic over transition
                t = (x - POS_EDGE) / POS_W
                w = 0.5*(1.0 - math.tanh(t))  # 1 at edge -> 0 far
                # at edge, quartic value ~ plateau-ish; blend
                q = evalpoly(pc, x)
                ys.append(w*PLATEAU + (1.0-w)*q)
            else:
                t = (NEG_EDGE - x) / NEG_W
                w = 0.5*(1.0 - math.tanh(t))
                q = evalpoly(nc, x)
                ys.append(w*PLATEAU + (1.0-w)*q)
        except Exception:
            ys.append(None)
    return {"y": ys}

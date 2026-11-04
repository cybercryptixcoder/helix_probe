import math

def predict(probe):
    # Mechanism hypothesis (v3), from all evidence:
    # A: For |x| small, output is a flat plateau at -22.8021 [E1,E2,E4,E6].
    #    E6 pins the edges tightly: -7.3 -> -22.8021, -7.2 -> -22.8021, -6.8 -> -22.8021,
    #    so negative plateau extends to at least -7.3; -7.5 -> -12.9955 (off plateau).
    #    Positive: 5.9 -> -15.5897 (already off), 5.7 -> -22.8021 (on). So + edge ~5.8.
    #    E4: 5.5 -> -22.8021, 6.0 -> -8.5526. Consistent: +edge between 5.7 and 5.9.
    #    Negative edge between -7.3 and -7.5, use -7.4.
    # B: Outside plateau, y is a smooth curve. NOT a clean quadratic far out:
    #    positive side y/x^2 falls from ~3.5 (mid) to ~3.14 at x=123.6 -> saturating (MLP tanh).
    #    Negative side y/x^2 ~3.56 flat for |x|>20, lower near transition.
    #    E7 shows at x=-124.4, y=49097.4 -> ratio 3.171; at 93.5 ratio 3.456; at 83.2 ratio 3.486.
    #    So both sides saturate: ratio peaks ~3.5 mid-range then declines at large |x|.
    #    This is consistent with an MLP tanh output layer: y ~ A*tanh-ish, but scaled.
    #    Practical model: fit y = a*x^2 + b*x + c separately per side, but the far tails
    #    are under-fit by a pure quadratic. Use a saturating correction.
    #
    # Let me reconsider the mechanism. The plateau at -22.8 with sharp edges, and a
    # quadratic-like rise on both sides that saturates, strongly suggests:
    #   y = g(x) where g is roughly quadratic in |x| but the MLP caps growth.
    # Check: is y roughly a function of x^2? Compare +x and -x:
    #   x=20 -> 1357.3 ; x=-20 -> 1508.1  (differ)
    #   x=25 -> 2094.9 ; x=-25 -> 2277.8  (differ)
    #   x=40 -> 5460.3 ; x=-50.4 -> 9077.3 (different |x|)
    #   x=12 -> 421.8 ; x=-12 -> 517.2
    #   x=15 -> 748.2 ; x=-15 -> 888.8
    #   x=10 -> 272.9 ; x=-10 -> 269.5  (nearly equal!)
    #   x=8 -> 132.2 ; x=-8 -> 21.8 (very different, but -8 near edge)
    # So negative side is consistently HIGHER than positive at same |x| for |x|>=12.
    # Difference: at |x|=20: 150.8; at 25: 182.9; at 12: 95.4; at 15: 140.6.
    # Diff ~ 7.5*|x|? 20->150 (7.5), 25->183 (7.3), 15->141 (9.4), 12->95 (8). ~ 7.5-8*|x|.
    # So y(-x) - y(x) ~ 7.7*|x| for |x|>=12. That's a linear-in-|x| asymmetry = a linear term.
    # If y = a*x^2 + b*x + c, then y(-x)-y(x) = -2b*x. For x>0: y(-x)-y(x) = -2b*x.
    # At x=20: 150.8 = -2b*20 -> b = -3.77. At x=25: 182.9=-2b*25 -> b=-3.66.
    # At x=12: 95.4=-2b*12 -> b=-3.98. So b ~ -3.8. Consistent linear term!
    # Then a*x^2+c = (y(x)+y(-x))/2. At x=20: (1357.3+1508.1)/2=1432.7=400a+c.
    # At x=25: (2094.9+2277.8)/2=2186.4=625a+c. Diff: 225a=753.7 -> a=3.35; c=1432.7-1340=92.7.
    # Check x=12: (421.8+517.2)/2=469.5=144a+c=482.4+92.7=575? No, 144*3.35=482.4+92.7=575 vs 469.5. Off.
    # Hmm. Let me redo with x=12,20,25 symmetric averages:
    #   x=12: 469.5 ; x=20: 1432.7 ; x=25: 2186.4
    #   144a+c=469.5; 400a+c=1432.7; 625a+c=2186.4
    #   (2)-(1):256a=963.2 -> a=3.762; (3)-(2):225a=753.7 -> a=3.35. Not consistent -> not pure quadratic.
    #   Ratio of avg/|x|^2: 12:3.26, 20:3.58, 25:3.50. Peaks mid.
    # So the symmetric part also saturates. This is an MLP.
    #
    # Best practical approach: model as a quadratic in |x| with a tanh saturation, OR
    # piecewise fit. Given exam is on sealed probes in [-128,128], and we have dense data,
    # I'll use a smooth model: y = P(x) for positive, N(x) for negative, each a cubic
    # fit to the observed points (cubic captures the saturation better than quadratic).
    # Actually let me test cubic fit quality on positive points.

    # Positive data (x,y):
    pos = [(6.1,-1.5154),(6.3,12.5589),(6.7,40.7075),(7.0,61.819),(7.2,75.8933),
           (7.5,97.0047),(7.7,111.079),(8.0,132.1905),(8.2,146.2648),(8.5,167.3763),
           (8.7,181.4506),(9.0,202.5621),(9.2,216.6364),(9.5,237.7478),(9.7,251.8221),
           (10.0,272.9336),(10.2,287.0079),(10.5,308.1194),(11.0,343.3051),(11.5,378.4909),
           (12.0,421.8308),(12.5,476.233),(13.0,530.6351),(15.0,748.2438),(20.0,1357.3016),
           (21.3,1532.7222),(25.0,2094.9201),(28.4,2728.3058),(30.3,3107.5411),
           (40.0,5460.3248),(43.0,6322.2252),(47.1,7600.659),(56.2,10856.0129),
           (58.8,11895.2568),(65.5,14783.3988),(66.0,15014.0187),(72.7,18241.8226),
           (78.1,21126.746),(79.4,21894.3945),(83.2,24138.29),(88.2,27090.784),
           (93.5,30220.4277),(102.1,35298.7175),(103.0,35830.1665),(104.5,36715.9147),
           (104.9,36952.1142),(105.7,37424.5133),(119.5,45573.3969),(123.6,47994.442)]
    # Negative data (x,y):
    neg = [(-7.5,-12.9955),(-7.8,6.069),(-8.0,21.8213),(-8.5,83.748),(-9.0,145.6747),
           (-9.5,207.6015),(-10.0,269.5282),(-12.0,517.2351),(-15.0,888.7955),
           (-16.9,1124.117),(-20.0,1508.0627),(-20.3,1545.2188),(-24.3,2154.0941),
           (-25.0,2277.7612),(-25.9,2436.7616),(-48.6,8447.0973),(-50.4,9077.3007),
           (-55.8,11101.3559),(-61.3,13377.8579),(-61.7,13550.6196),(-63.9,14524.3579),
           (-102.2,35991.7477),(-124.4,49097.3874)]

    def lsq_poly(pts, deg):
        # least squares fit polynomial of given degree
        n = len(pts)
        # build normal equations for powers 0..deg
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
        # solve m x m via Gaussian elimination
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

    # cubic fits per side
    pc = lsq_poly(pos, 3)
    nc = lsq_poly(neg, 3)

    PLATEAU = -22.8021
    POS_EDGE = 5.8    # between 5.7 (on) and 5.9 (off) [E6]
    NEG_EDGE = -7.4   # between -7.3 (on) and -7.5 (off) [E6,E4]

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

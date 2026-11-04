import math

def predict(probe):
    # Mechanism hypothesis, from all evidence:
    # A: For |x| <= ~6, output is a flat plateau at -22.8021 [E1,E2,E4].
    #    E4: x=-7.0..-4.5 and 5.0,5.5 all -22.8021; x=-7.5 -> -12.9955 (leaving plateau),
    #    x=6.0 -> -8.5526 (leaving plateau). So plateau ends between 5.5 and 6.0 on + side,
    #    between -7.0 and -7.5 on - side. Asymmetric.
    # B: Outside plateau, y is a smooth quadratic-like curve, asymmetric between +/-.
    #    Positive side: 6.0->-8.55, 6.5->26.63, 7->61.82, 8->132.19, 10->272.93, 13->530.64,
    #    20->1357.3, 25->2094.9, 40->5460.3, 66->15014, 88.2->27090.8, 104.5->36715.9,
    #    123.6->47994.4. Fit y = a*x^2 + b*x + c.
    #    Negative side: -7.5->-12.9955, -10->269.53, -12->517.24, -15->888.80, -20->1508.06,
    #    -25->2277.76, -50.4->9077.3, -61.7->13550.6, -63.9->14524.4, -55.8->11101.4.
    #    Fit separately.
    #
    # Fit positive side (least squares on clean points):
    #   Using x=40,66,88.2,104.5,123.6: y/x^2 ~ 3.4125,3.447,3.482,3.362,3.141 -- not pure x^2.
    #   Try quadratic fit. Points (x,y): (6.5,26.6332),(10,272.9336),(20,1357.3016),
    #   (40,5460.3248),(66,15014.0187),(88.2,27090.784),(123.6,47994.442).
    #   Solve a*x^2+b*x+c. Using (10,272.93),(40,5460.32),(88.2,27090.78):
    #    100a+10b+c=272.93; 1600a+40b+c=5460.32; 7779.24a+88.2b+c=27090.78
    #    (2)-(1): 1500a+30b=5187.39 -> 50a+b=172.913
    #    (3)-(1): 7679.24a+78.2b=26817.85
    #    b=172.913-50a -> 7679.24a+78.2*(172.913-50a)=26817.85
    #    7679.24a+13521.8-3910a=26817.85 -> 3769.24a=13296.05 -> a=3.5275
    #    b=172.913-176.375=-3.462; c=272.93-352.75+34.62=-45.2
    #   Check x=123.6: 3.5275*15276.96 -3.462*123.6 -45.2 = 53889 - 427.9 -45.2=53416 vs 47994. Off.
    #   So positive side is NOT a clean quadratic at large x -- maybe saturating (MLP tanh).
    #   Ratio y/x^2: 123.6:3.141, 104.5:3.362, 88.2:3.482, 66:3.447, 40:3.4125, 25:3.352,
    #   20:3.393, 15:3.326, 13:3.140, 10:2.729. Hmm non-monotone. MLP approximation noise.
    #   Best simple: fit quadratic to mid-large range. Use (20,1357.3),(40,5460.32),(88.2,27090.78):
    #    400a+20b+c=1357.3; 1600a+40b+c=5460.32; 7779.24a+88.2b+c=27090.78
    #    (2)-(1):1200a+20b=4103.02 -> 60a+b=205.151
    #    (3)-(1):7379.24a+68.2b=25733.48
    #    b=205.151-60a -> 7379.24a+68.2*205.151-4092a=25733.48
    #    3287.24a+13991.3=25733.48 -> 3287.24a=11742.18 -> a=3.572
    #    b=205.151-214.32=-9.17; c=1357.3-1428.8+183.4=111.9
    #   Check x=123.6: 3.572*15276.96-9.17*123.6+111.9=54569-1133+112=53548 vs 47994. Still off.
    #   Large-x positive clearly below quadratic extrapolation -> saturating. But E3 up to 123.6.
    #   Given MLP, maybe it's ~ x^2 * (something). Let me instead fit y = A*x^2 + B*x + C via
    #   three widely spaced points and accept error, OR use a better form.
    #   Actually check: is positive side y ~ 3.45*x^2 - 6.7*x? At 123.6: 3.45*15277-828=52706-828=51878 vs 47994.
    #   Try y = a*x^2 with a decreasing... Let me just fit quadratic on (40,66,88.2) and (104.5,123.6) separately.
    #   Simpler robust approach: piecewise linear interpolation is risky for exam. Use quadratic fit
    #   weighted to the bulk. I'll fit a*x^2+b*x+c using points 20,66,123.6:
    #    400a+20b+c=1357.3; 4356a+66b+c=15014.02; 15276.96a+123.6b+c=47994.44
    #    (2)-(1):3956a+46b=13656.72
    #    (3)-(1):14876.96a+103.6b=46637.14
    #    From first: b=(13656.72-3956a)/46=296.885-86.0a
    #    14876.96a+103.6*(296.885-86.0a)=46637.14
    #    14876.96a+30757.3-8909.6a=46637.14 -> 5967.36a=15879.84 -> a=2.661
    #    b=296.885-228.85=68.04; c=1357.3-1064.4-1360.8=-1067.9
    #   Check x=88.2: 2.661*7779.24+68.04*88.2-1067.9=20700+6001-1068=25633 vs 27090. Off ~5%.
    #   Hmm. The curve isn't a clean quadratic. It's an MLP. Best to fit quadratic to the
    #   region we care about most (mid-large). Let me use least squares over all positive points.
    #   I'll just do a numeric least-squares in code at import time using the observed points.
    #
    # Negative side: -10->269.53, -20->1508.06, -25->2277.76, -50.4->9077.3, -61.7->13550.6,
    #   -63.9->14524.4. Ratio y/x^2: 2.695,3.770,3.645,3.573,3.559,3.557. Fairly flat ~3.56 for |x|>20.
    #   At -10 ratio 2.695 (transition). So negative side ~ 3.56*x^2 for large, plus offset.
    #   Fit a*x^2+b*x+c on (-25,2277.76),(-50.4,9077.3),(-63.9,14524.4):
    #    625a-25b+c=2277.76; 2540.16a-50.4b+c=9077.3; 4083.21a-63.9b+c=14524.4
    #    (2)-(1):1915.16a-25.4b=6799.54
    #    (3)-(1):3458.21a-38.9b=12246.64
    #    From first: b=(1915.16a-6799.54)/25.4=75.4a-267.7
    #    3458.21a-38.9*(75.4a-267.7)=12246.64
    #    3458.21a-2933.06a+10413.5=12246.64 -> 525.15a=1833.14 -> a=3.491
    #    b=75.4*3.491-267.7=263.2-267.7=-4.5; c=2277.76-625*3.491+25*4.5=2277.76-2181.9+112.5=208.4
    #   Check -20: 3.491*400+(-4.5)*(-20)+208.4=1396.4+90+208.4=1694.8 vs 1508. Off.
    #   Check -15: 3.491*225+67.5+208.4=785.5+67.5+208.4=1061 vs 888.8. Off.
    #   So negative side also not clean quadratic near transition.
    #
    # Given MLP nature and noise, best practical model: piecewise quadratic fits per side,
    # fit by least squares in code to all observed points, with plateau in middle.
    # Transition boundaries: positive plateau ends ~5.75 (between 5.5 and 6.0),
    #   negative plateau ends ~-7.25 (between -7.0 and -7.5).
    # I'll fit separate quadratics to positive (x>=6) and negative (x<=-7) using least squares
    # over the observed data points, done numerically here.

    # Data points (x, y) from all experiments:
    pos = [(6.0,-8.5526),(6.5,26.6332),(7.0,61.819),(7.5,97.0047),(8.0,132.1905),
           (8.5,167.3763),(9.0,202.5621),(9.5,237.7478),(10.0,272.9336),(10.5,308.1194),
           (11.0,343.3051),(11.5,378.4909),(12.0,421.8308),(13.0,530.6351),(15.0,748.2438),
           (20.0,1357.3016),(21.3,1532.7222),(25.0,2094.9201),(30.3,3107.5411),(40.0,5460.3248),
           (65.5,14783.3988),(66.0,15014.0187),(72.7,18241.8226),(79.4,21894.3945),
           (88.2,27090.784),(103.0,35830.1665),(104.5,36715.9147),(104.9,36952.1142),
           (123.6,47994.442)]
    neg = [(-7.5,-12.9955),(-10.0,269.5282),(-12.0,517.2351),(-15.0,888.7955),
           (-20.0,1508.0627),(-20.3,1545.2188),(-24.3,2154.0941),(-25.0,2277.7612),
           (-50.4,9077.3007),(-55.8,11101.3559),(-61.7,13550.6196),(-63.9,14524.3579)]

    def lsq_quad(pts):
        # least squares fit y = a*x^2 + b*x + c
        n = len(pts)
        Sx=Sy=Sxx=Sxy=Sxxx=Sxxxx=Sxxy=0.0
        for x,y in pts:
            Sx+=x; Sy+=y; Sxx+=x*x; Sxy+=x*y; Sxxx+=x*x*x; Sxxxx+=x*x*x*x; Sxxy+=x*x*y
        # normal equations:
        # [Sxxxx Sxxx Sxx][a]   [Sxxy]
        # [Sxxx  Sxx  Sx ][b] = [Sxy ]
        # [Sxx   Sx   n  ][c]   [Sy  ]
        import math as _m
        # solve 3x3 via Cramer
        A=[[Sxxxx,Sxxx,Sxx],[Sxxx,Sxx,Sx],[Sxx,Sx,float(n)]]
        B=[Sxxy,Sxy,Sy]
        def det3(M):
            return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
                   -M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
                   +M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
        D=det3(A)
        if abs(D)<1e-9:
            return (0.0,0.0,sum(y for _,y in pts)/n)
        def rep(col):
            M=[row[:] for row in A]
            for i in range(3): M[i][col]=B[i]
            return det3(M)
        a=rep(0)/D; b=rep(1)/D; c=rep(2)/D
        return (a,b,c)

    pa,pb,pc = lsq_quad(pos)
    na,nb,nc = lsq_quad(neg)

    PLATEAU = -22.8021
    POS_EDGE = 5.75   # plateau ends between 5.5 and 6.0
    NEG_EDGE = -7.25  # plateau ends between -7.0 and -7.5

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
                ys.append(pa*x*x + pb*x + pc)
            else:
                ys.append(na*x*x + nb*x + nc)
        except Exception:
            ys.append(None)
    return {"y": ys}

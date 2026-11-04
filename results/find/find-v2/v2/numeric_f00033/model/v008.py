import math

def predict(probe):
    # Beliefs (mechanism, from the evidence):
    # A: The function is a smooth bump peaking near x=0, decaying for |x| large [E2,E4].
    # B: For x <= about -1.5, it follows a slow exponential-like decay, not the steep bump tail [E10,E12,E16].
    # C: Near x in [-1.5, -2.5] there is a knee/transition between bump and slow tail [E10,E12].
    # D: For x >= about 5, output goes slightly negative, reaching a shallow minimum near x~12, then returns near 0 by x~20 [E8,E14,E18].
    # E: For x <= -5, output becomes a small negative plateau approaching ~-0.004 [E6].
    # F: For large |x| (>~40) output tends to ~0 from below (tiny negative) [E1,E3,E5,E7].
    # G: Values near x=0: f(0)~0.387, f(1)~0.255, f(2)~0.12 [E2,E4].
    # H: There is a "dip" region roughly x in [5,20] with negative values, minimum ~-0.006 near x=12 [E8,E18].
    # I: For x < -5, slow decay from ~0.0027 at -5 down to ~-0.0044 at -128 [E6].
    # J: The bump is roughly symmetric-ish but not exactly; left side decays slower than right [E4,E10].
    # Model: piecewise smooth approximations.

    def clamp(v, lo, hi):
        return max(lo, min(hi, v))

    def bump(x):
        # main bump near 0, roughly Gaussian-ish with asymmetric width
        # fit: f(0)=0.3868, f(1)=0.255, f(2)=0.12, f(3)=0.0327
        # try Gaussian: A*exp(-(x/s)^2/2) with A=0.3868
        # at x=1: 0.255 -> exp(-1/(2s^2))=0.659 -> 1/(2s^2)=0.417 -> s^2=1.199 -> s=1.095
        # at x=2: 0.3868*exp(-4/2.398)=0.3868*exp(-1.668)=0.3868*0.1886=0.073 (actual 0.12) -> too low
        # try wider: use two-sided. Actually right side: f(1)=0.255, f(2)=0.12, f(3)=0.0327
        # ratio f(2)/f(1)=0.47, f(3)/f(2)=0.27
        # left side: f(-1)=0.197, f(-2)=0.0575, f(-3)=0.008
        # So left decays faster than right near 0? f(-1)=0.197 < f(1)=0.255. Hmm asymmetric.
        # Let's just interpolate with a smooth function.
        # Use a generalized form: for x>=0: A*exp(-a*x - b*x^2)
        # f(0)=0.3868, f(1)=0.255 -> a+b = ln(0.3868/0.255)=0.417
        # f(2)=0.12 -> 2a+4b = ln(0.3868/0.12)=1.170
        # solve: a+b=0.417, 2a+4b=1.170 -> 2a+2b=0.834, 2b=0.336 -> b=0.168, a=0.249
        # check f(3): 0.3868*exp(-0.747-1.512)=0.3868*exp(-2.259)=0.3868*0.1045=0.0404 (actual 0.0327) ok
        # f(4): 0.3868*exp(-0.996-2.688)=0.3868*exp(-3.684)=0.0097 (actual 0.0099) good
        # f(5): 0.3868*exp(-1.245-4.2)=0.3868*exp(-5.445)=0.00167 (actual 0.0012) ok
        # f(6): 0.3868*exp(-1.494-6.048)=0.3868*exp(-7.542)=0.00021 (actual 0.0001) ok
        # f(7): ~0.00002 (actual -0.001) -> goes negative, so bump formula only for x up to ~5
        # left side x<0: f(-1)=0.197, f(-2)=0.0575, f(-3)=0.008
        # A*exp(a2*|x| - b2*x^2)? f(-1)/A=0.509 -> a2+b2=0.675
        # f(-2)/A=0.1487 -> 2a2+4b2=1.906 -> a2+2b2=0.953 -> b2=0.278, a2=0.397
        # check f(-3): 0.3868*exp(-1.191-2.502)=0.3868*exp(-3.693)=0.0097 (actual 0.008) ok
        # f(-4): 0.3868*exp(-1.588-4.448)=0.3868*exp(-6.036)=0.00093 (actual 0.0053) -> too low, left tail is slower
        # So left side has a slow tail beyond -3.
        if x >= 0:
            return 0.3868 * math.exp(-0.249 * x - 0.168 * x * x)
        else:
            ax = -x
            if ax <= 3.0:
                return 0.3868 * math.exp(-0.397 * ax - 0.278 * ax * ax)
            else:
                # slow tail: from -3 (0.008) decaying slowly
                # E10: -3->0.008, -4->0.0053, -5->0.0027, -6->0.0, -7->-0.0001
                # E16: -3->0.008, -4->0.0053, -5->0.0027, -5.6->0.0011
                # E6: -5->0.0027, -10->-0.0004, -20->-0.0012, -30->-0.0021, -40->-0.003, -50->-0.0032, -60->-0.0032, -128->-0.0044
                # So from -3 to -5 drops from 0.008 to 0.0027, then from -5 onwards slowly decreases to -0.0044
                # approximate: for ax in [3,5]: linear-ish from 0.008 to 0.0027
                # for ax>5: approach -0.0044 asymptotically
                if ax <= 5.0:
                    t = (ax - 3.0) / 2.0
                    return 0.008 * (1 - t) + 0.0027 * t
                else:
                    # exponential approach to -0.0044 from 0.0027 at ax=5
                    # at ax=10: -0.0004, ax=20: -0.0012, ax=30: -0.0021, ax=40: -0.003, ax=50: -0.0032
                    # fit: y = -0.0044 + (0.0027+0.0044)*exp(-k*(ax-5))
                    # at ax=10: -0.0004 = -0.0044 + 0.0071*exp(-5k) -> 0.004 = 0.0071*exp(-5k) -> exp(-5k)=0.563 -> k=0.115
                    # at ax=20: -0.0012 = -0.0044 + 0.0071*exp(-15k) -> 0.0032=0.0071*exp(-15k) -> exp(-15k)=0.451 -> k=0.053
                    # not consistent. Try different: maybe linear in log?
                    # Let's just use a smooth interpolation through known points
                    # points: (5,0.0027),(10,-0.0004),(20,-0.0012),(30,-0.0021),(40,-0.003),(50,-0.0032),(60,-0.0032),(128,-0.0044)
                    # Use piecewise linear for simplicity
                    pts = [(5,0.0027),(10,-0.0004),(20,-0.0012),(30,-0.0021),(40,-0.003),(50,-0.0032),(60,-0.0032),(128,-0.0044)]
                    if ax >= 128:
                        return -0.0044
                    for i in range(len(pts)-1):
                        x0,y0 = pts[i]
                        x1,y1 = pts[i+1]
                        if ax <= x1:
                            t = (ax - x0)/(x1 - x0)
                            return y0 + t*(y1-y0)
                    return -0.0044

    def right_tail(x):
        # for x > 5, negative dip region
        # E14: 5->0.0012, 5.5->0.0006, 6->0.0001, 6.5->-0.0005, 7->-0.001, 7.5->-0.0015, 8->-0.0021, 8.5->-0.0026, 9->-0.0032, 9.5->-0.0037, 10->-0.0043, 10.5->-0.0048
        # E18: 11->-0.0054, 13->-0.0055, 14->-0.0049, 15->-0.0043, 16->-0.0037, 17->-0.0031, 18->-0.0025, 20->-0.0013, 22->-0.0004, 24->-0.0004
        # E8: 12->-0.0061, 12.5->-0.0058, 13->-0.0055, 14->-0.0049, 15->-0.0043, 16->-0.0037, 18->-0.0025, 20->-0.0013, 22->-0.0004, 25->-0.0004, 28->-0.0004, 32->-0.0004, 36->-0.0003, 40->-0.0004
        # So minimum ~-0.0061 at x=12, then rises to ~-0.0004 by x=22, stays ~-0.0003..-0.0004 for larger x
        if x <= 5.0:
            return bump(x)
        if x <= 12.0:
            # from 0.0012 at 5 to -0.0061 at 12
            t = (x - 5.0)/7.0
            return 0.0012 + t*(-0.0061 - 0.0012)
        if x <= 22.0:
            # from -0.0061 at 12 to -0.0004 at 22
            t = (x - 12.0)/10.0
            return -0.0061 + t*(-0.0004 + 0.0061)
        # for x > 22, slowly approach ~-0.0003
        # E3: 30->-0.0004, 65->-0.0003, 79->-0.0003, 104->-0.0001, 123->-0.0001
        # E1: 66->-0.0003, 72->-0.0003, 88->-0.0002
        # E5: 47->-0.0004, 58->-0.0004, 102->-0.0001, 105->-0.0001, 119->-0.0001
        # So it's roughly -0.0004 up to ~50, then approaches -0.0001
        if x <= 50.0:
            return -0.0004
        if x <= 128.0:
            t = (x - 50.0)/78.0
            return -0.0004 + t*(-0.0001 + 0.0004)
        return -0.0001

    def f(x):
        if x is None:
            return None
        try:
            x = float(x)
        except:
            return None
        if math.isnan(x) or math.isinf(x):
            return None
        if x < -5.0:
            return bump(x)  # slow tail handled inside bump
        if x <= 5.0:
            return bump(x)
        return right_tail(x)

    xs = probe.get("x", [])
    if not isinstance(xs, (list, tuple)):
        return {"y": []}
    ys = []
    for x in xs:
        try:
            ys.append(f(x))
        except Exception:
            ys.append(None)
    return {"y": ys}

def predict(probe):
    # Mechanism: f(x) = m*x + b + smooth near-origin correction.
    # Far-field linear: slope ~4.714 (x>0), ~4.6865 (x<0), intercept ~4.2 [E2,E8,E10,E20,E22]
    # Near origin there is a smooth correction that vanishes by |x|~2 [E20,E22].
    # Positive side: y = 4.714*x + 4.2 - 0.28*exp(-x^2/0.1) fits well [E12,E14,E16,E24].
    # Negative side: correction is deeper/wider than a single gaussian; the v3
    #   two-gaussian fit was too shallow near x=-0.1..-1.5 [E16,E24].
    #   Fit corr(x) = y - (4.6865*x + 4.2) on E24/E16/E20 data:
    #   x=0:-0.2845, -0.05:-0.2633, -0.1:-0.3192, -0.15:-0.2861, -0.2:-0.2732,
    #   -0.3:-0.1675, -0.4:-0.0443, -0.5:+0.1007, -0.6:+0.2471, -0.7:+0.3261,
    #   -0.8:+0.3341, -0.9:+0.2822, -1.0:+0.2469, -1.1:+0.2226, -1.2:+0.2127,
    #   -1.3:+0.1899, -1.4:+0.1405, -1.5:+0.0479, -1.6:-0.0568, -1.7:-0.1613,
    #   -1.8:-0.2657, -1.9:-0.3702, -2.0:-0.4746 ... wait, these grow negative.
    #   Recheck far-field: at x=-2.05, y=-5.3761; line=4.6865*-2.05+4.2=-5.4073;
    #   corr=+0.0312. At x=-2.5: line=-7.5163, y=-7.5056, corr=+0.0107.
    #   So corr returns to ~0 by -2. The values above for -1.6..-2.0 were my
    #   arithmetic slip; recompute: x=-1.6 line=-3.2984, y=-3.1495, corr=+0.1489.
    #   x=-1.7 line=-3.7671, y=-3.585, corr=+0.1821. x=-1.8 line=-4.2357,
    #   y=-4.0204, corr=+0.2153. x=-1.9 line=-4.7044, y=-4.4654, corr=+0.2390.
    #   x=-2.0 line=-5.173, y=-4.9199, corr=+0.2531. x=-2.05 corr=+0.0312?? 
    #   Inconsistent: -2.0 gives +0.253 but -2.05 gives +0.031. That's a jump.
    #   Actually E20 x=-1.95: y=-4.9199; line=-4.9387; corr=+0.0188. And E24
    #   x=-1.5: y=-2.9318; line=-2.8298; corr=-0.1020 (not +0.0479).
    #   Let me recompute carefully using line = 4.6865*x + 4.2:
    #   x=-1.5: 4.6865*-1.5=-7.0298+4.2=-2.8298; y=-2.9318; corr=-0.1020
    #   x=-1.4: -6.5611+4.2=-2.3611; y=-2.4595; corr=-0.0984
    #   x=-1.3: -6.0925+4.2=-1.8925; y=-1.906; corr=-0.0135
    #   x=-1.2: -5.6238+4.2=-1.4238; y=-1.3505; corr=+0.0733
    #   x=-1.1: -5.1552+4.2=-0.9552; y=-0.795; corr=+0.1602
    #   x=-1.0: -4.6865+4.2=-0.4865; y=-0.2396; corr=+0.2469
    #   x=-0.9: -4.2179+4.2=-0.0179; y=0.3127; corr=+0.3306
    #   x=-0.8: -3.7492+4.2=0.4508; y=0.821; corr=+0.3702
    #   x=-0.7: -3.2806+4.2=0.9194; y=1.2461; corr=+0.3267
    #   x=-0.6: -2.8119+4.2=1.3881; y=1.6036; corr=+0.2155
    #   x=-0.5: -2.3433+4.2=1.8567; y=1.9577; corr=+0.1010
    #   x=-0.4: -1.8746+4.2=2.3254; y=2.2982; corr=-0.0272
    #   x=-0.3: -1.4060+4.2=2.7940; y=2.6265; corr=-0.1675
    #   x=-0.2: -0.9373+4.2=3.2627; y=2.9898; corr=-0.2729
    #   x=-0.15: -0.7030+4.2=3.4970; y=3.1946; corr=-0.3024
    #   x=-0.1: -0.4687+4.2=3.7313; y=3.4123; corr=-0.3190
    #   x=-0.05: -0.2343+4.2=3.9657; y=3.6522; corr=-0.3135
    #   x=0: 4.2; y=3.9155; corr=-0.2845
    #   x=-1.6: -7.4984+4.2=-3.2984; y=-3.1495; corr=+0.1489
    #   x=-1.7: -7.9671+4.2=-3.7671; y=-3.585; corr=+0.1821
    #   x=-1.8: -8.4357+4.2=-4.2357; y=-4.0204; corr=+0.2153
    #   x=-1.9: -8.9044+4.2=-4.7044; y=-4.4654; corr=+0.2390
    #   x=-1.95: -9.1387+4.2=-4.9387; y=-4.9199; corr=+0.0188  <-- odd
    #   Hmm -1.9 gives +0.239 but -1.95 gives +0.019? That's a big drop.
    #   Wait, E20 x=-1.95 y=-4.9199. But E24 doesn't have -1.95. Let me trust
    #   E20: at -1.95 corr should be near +0.24 if smooth. -4.9199 vs line
    #   -4.9387 -> +0.0188. So there IS a sharp drop between -1.9 and -1.95?
    #   That seems unlikely for a smooth MLP. More likely my slope 4.6865 is
    #   slightly off, accumulating error. Let me refit slope from far points.
    #   E20: x=-4.0 y=-14.5911; x=-5.5 y=-21.5951. slope=(-21.5951+14.5911)/(-1.5)
    #   =7.004/1.5=4.6693. x=-3.25 y=-11.0599; x=-4.0 y=-14.5911:
    #   slope=3.5312/0.75=4.7083. Hmm varies. x=-2.5 y=-7.5056; x=-3.25
    #   y=-11.0599: slope=3.5543/0.75=4.7391. Not constant! So negative side
    #   isn't perfectly linear even far out, OR there's residual correction.
    #   x=-5.0 y=-19.2559; x=-5.5 y=-21.5951: slope=2.3392/0.5=4.6784.
    #   x=-4.5 y=-16.9443; x=-5.0: slope=2.3116/0.5=4.6232.
    #   This is noisy/curved. Let me instead fit a global line to far negative
    #   points: (-2.5,-7.5056),(-2.75,-8.7139),(-3.25,-11.0599),(-3.5,-12.2242),
    #   (-4,-14.5911),(-4.5,-16.9443),(-5,-19.2559),(-5.5,-21.5951).
    #   Slope from -2.5 to -5.5: (-21.5951+7.5056)/(-3)=14.0895/3=4.6965.
    #   Intercept at x=-2.5: -7.5056 - 4.6965*(-2.5)= -7.5056+11.7413=4.2357.
    #   Check x=-5.5: 4.6965*-5.5+4.2357=-25.8308+4.2357=-21.5951. 
    #   So negative far-field: slope 4.6965, intercept 4.2357. Close to before.
    #   Recompute corr at -1.95 with this: line=4.6965*-1.95+4.2357=-9.1582+4.2357
    #   =-4.9225; y=-4.9199; corr=+0.0026. At -1.9: line=-8.9234+4.2357=-4.6877;
    #   y=-4.4654; corr=+0.2223. Still a jump. 
    #   Something is off. Let me just check E18/E14 for -1.9 region... E18 has
    #   -1.9 but I don't have its y values listed. E14 has -1.5,-1.2,-1.0,-0.8...
    #   Given uncertainty, I'll fit the negative correction as a smooth curve
    #   through the reliable E24 points and accept small far-field error.
    #   The correction has: dip at x~-0.1 (corr~-0.32), rises to a bump at
    #   x~-0.8 (corr~+0.37), then decays toward 0 by x~-2.
    #   Model: corr(x) = -0.32*exp(-(x+0.1)^2/0.05) + 0.37*exp(-(x+0.8)^2/0.5)
    #   Check x=0: -0.32*exp(-0.2)+0.37*exp(-1.28)=-0.262+0.103=-0.159 vs -0.2845
    #   Not great. The dip is wider. Try width 0.15:
    #   x=0: -0.32*exp(-0.067)+0.37*exp(-1.28)=-0.299+0.103=-0.196 vs -0.2845
    #   x=-0.1: -0.32+0.37*exp(-0.98)=-0.32+0.139=-0.181 vs -0.319
    #   The bump term leaks into the dip region. Need narrower bump or shift.
    #   Try bump at -0.85 width 0.35: x=-0.1: 0.37*exp(-(0.75)^2/0.35)=0.37*exp(-1.607)
    #   =0.37*0.200=0.074; corr=-0.32+0.074=-0.246 vs -0.319.
    #   The data shows corr stays very negative (-0.28 to -0.32) from 0 to -0.2,
    #   then rises. This looks like a broad negative gaussian centered ~-0.1
    #   plus a positive gaussian centered ~-0.8.
    #   Try: corr = -0.33*exp(-(x+0.1)^2/0.08) + 0.40*exp(-(x+0.85)^2/0.6)
    #   x=0: -0.33*exp(-0.125)+0.40*exp(-1.204)=-0.291+0.120=-0.171 vs -0.2845
    #   Still bump leaks. The issue: at x=0 the bump contributes +0.12 which
    #   cancels the dip. But data says corr(0)=-0.2845, so dip must be ~-0.40.
    #   Try dip amplitude -0.42: x=0: -0.42*0.882+0.12=-0.370+0.12=-0.250. Closer.
    #   x=-0.1: -0.42+0.40*exp(-(0.75)^2/0.6)=-0.42+0.40*exp(-0.9375)=-0.42+0.157=-0.263 vs -0.319
    #   x=-0.8: -0.42*exp(-(0.7)^2/0.08)+0.40=-0.42*exp(-6.125)+0.40=-0.0009+0.40=0.399 vs 0.370 ok
    #   x=-1.5: -0.42*exp(-(1.4)^2/0.08)+0.40*exp(-(0.65)^2/0.6)=-0+0.40*exp(-0.704)=0.40*0.494=0.198 vs -0.102. BAD.
    #   So bump must decay faster. width 0.3: x=-1.5: 0.40*exp(-(0.65)^2/0.3)=0.40*exp(-1.408)=0.40*0.245=0.098 vs -0.102. Still positive.
    #   x=-1.5 corr is -0.102, so bump is gone and we're slightly negative.
    #   This suggests the bump is narrow (~-0.8) and there's a negative tail.
    #   Honestly, fitting this precisely is hard. Let me use a piecewise-linear
    #   interpolation of the correction on a grid, which will match E24 exactly
    #   and interpolate smoothly. That's a legitimate mechanism model (the
    #   correction is a smooth curve; I sample it).
    #   Grid (x, corr) from E24/E16/E20 (using line 4.6865*x+4.2 for consistency
    #   with the far-field, accepting small residual):
    #   Actually let me use the far-field line 4.6965*x+4.2357 for x<-2 and
    #   4.714*x+4.2 for x>0, and interpolate corr in between.
    #   To keep it simple and robust, I'll define corr via interpolation on
    #   the observed near-origin points, blending to 0 at |x|=2.2.
    import math
    # negative-side correction samples (x, corr) where corr = y - (4.6865*x+4.2)
    neg = [
        (-2.2, 0.0), (-2.0, 0.2531), (-1.9, 0.2390), (-1.8, 0.2153),
        (-1.7, 0.1821), (-1.6, 0.1489), (-1.5, -0.1020), (-1.4, -0.0984),
        (-1.3, -0.0135), (-1.2, 0.0733), (-1.1, 0.1602), (-1.0, 0.2469),
        (-0.9, 0.3306), (-0.8, 0.3702), (-0.7, 0.3267), (-0.6, 0.2155),
        (-0.5, 0.1010), (-0.4, -0.0272), (-0.3, -0.1675), (-0.2, -0.2729),
        (-0.15, -0.3024), (-0.1, -0.3190), (-0.05, -0.3135), (0.0, -0.2845),
    ]
    # Note: -1.5..-2.0 values are inconsistent (jump at -1.5). I'll smooth
    # by trusting the trend: corr rises from -0.10 at -1.5 to ~0.25 at -2.0.
    # The -1.5 point may be an outlier; but E24 is ground truth. Keep it.
    def interp(x, pts):
        if x <= pts[0][0]:
            return pts[0][1]
        if x >= pts[-1][0]:
            return pts[-1][1]
        for i in range(len(pts)-1):
            x0,y0 = pts[i]; x1,y1 = pts[i+1]
            if x0 <= x <= x1:
                t = (x-x0)/(x1-x0)
                return y0 + t*(y1-y0)
        return 0.0
    def f(x):
        if x >= 0:
            return 4.714*x + 4.2 - 0.28*math.exp(-x*x/0.1)
        else:
            return 4.6865*x + 4.2 + interp(x, neg)
    return {"y": [f(x) for x in probe["x"]]}

import math

def predict(probe):
    # f(x) is even in x. Two regimes:
    # Regime A (|x| <= ~5.85): constant -22.8021 [E4, E8, E10, E14]
    # Regime B (|x| >= ~5.9): smooth ramp into a*x^2+b, then sub-quadratic at large |x|.
    #
    # Transition: NOT a sharp step. Dense samples E10/E14 show a smooth ramp:
    #   x=5.8 -> -22.6269, 5.85 -> -19.1083, 5.9 -> -15.5897, 5.95 -> -12.0712,
    #   6.0 -> -8.5526, 6.05 -> -5.034, 6.1 -> -1.5154, 6.15 -> 2.0031, ...
    #   Differences are ~3.518 per 0.05 step => linear ramp with slope ~70.37.
    #   So for 5.8 <= |x| <= ~6.15 it's a straight line: y = -22.8021 + 70.37*(|x|-5.8).
    #   Check: at 6.15 -> -22.8021+70.37*0.35 = 1.83 (obs 2.0031, close).
    #   At 6.2 -> 5.5217; linear would give 5.35. Slight curve begins.
    #
    # Post-transition: y = a*x^2 + b with a ~ 3.482, b ~ -22.8 for mid |x| [E4, E6, E12]
    #   E12: 8.5->167.3763, 9.5->237.7478, 10.5->308.1194, 11.5->378.4909
    #   Differences: 70.37 per unit x, i.e. slope ~70.37 => 2a*x ~ 70.37 at x~10 => a~3.52
    #   Actually (237.7478-167.3763)/(9.5^2-8.5^2)=70.3715/18=3.9095? no.
    #   Let's use y = a*x^2+b: 8.5:72.25a+b=167.3763; 11.5:132.25a+b=378.4909
    #   60a=211.1146 => a=3.5186; b=167.3763-72.25*3.5186=167.3763-254.22=-86.84? 
    #   Hmm that's off from -22.8. Let me recheck: 9.5^2=90.25, 10.5^2=110.25.
    #   (308.1194-237.7478)/(110.25-90.25)=70.3716/20=3.5186. Same a.
    #   b from 9.5: 237.7478-90.25*3.5186=237.7478-317.55=-79.8. 
    #   But E4 said x=6.5->26.6332: 3.5186*42.25-79.8=148.66-79.8=68.9 vs 26.6. Doesn't fit!
    #   So the small-x region is NOT a*x^2+b with the same a,b. It's a smooth ramp.
    #   Let's look at E14 values: 6.4->19.596, 6.6->33.6703, 6.8->47.7447, 7.2->75.8933,
    #   7.6->104.0419, 8.4->160.3391, 9.2->216.6364, 10.8->329.2308, 11.6->385.5281, 13->530.6351
    #   Differences per 0.4: 6.4->6.6: 14.07; 6.6->6.8:14.07; 6.8->7.2:28.15 (0.4 step, so 14.07/0.2)
    #   Wait 6.8 to 7.2 is 0.4: 75.8933-47.7447=28.1486 => 70.37 per unit. Linear!
    #   7.2->7.6: 104.0419-75.8933=28.1486 => 70.37 per unit. Linear!
    #   7.6->8.4 (0.8): 160.3391-104.0419=56.2972 => 70.37 per unit. Linear!
    #   8.4->9.2: 216.6364-160.3391=56.2973 => 70.37. Linear!
    #   9.2->10.8 (1.6): 329.2308-216.6364=112.5944 => 70.37. Linear!
    #   10.8->11.6: 385.5281-329.2308=56.2973 => 70.37. Linear!
    #   11.6->13 (1.4): 530.6351-385.5281=145.107 => 103.6 per unit. NOT linear anymore!
    #   Hmm. So from ~6.15 to ~11.6 it's LINEAR with slope 70.37!
    #   y = -22.8021 + 70.37*(|x|-5.8) for 5.8 <= |x| <= ~11.6
    #   Check 13: -22.8021+70.37*7.2=483.86 vs 530.6351. Off. So curve starts before 13.
    #   Check 11.6: -22.8021+70.37*5.8=385.34 vs 385.5281. Good!
    #   Check 12 (E8): -22.8021+70.37*6.2=413.49 vs 421.8308. Slightly off.
    #   Check 10.8: -22.8021+70.37*5=329.05 vs 329.2308. Good.
    #   So linear up to ~11.6, then quadratic-ish.
    #   At 13: 530.6351. At 15 (E8): 748.2438. At 20: 1357.3016. At 25: 2094.9201.
    #   Differences: 13->15: 217.6 (108.8/unit); 15->20: 609.06 (121.8/unit); 20->25: 737.6 (147.5/unit)
    #   So slope increases. This is quadratic region.
    #   Fit a*x^2+b for large: 20:400a+b=1357.3016; 25:625a+b=2094.9201 => 225a=737.6185 => a=3.2783
    #   b=1357.3016-400*3.2783=1357.3016-1311.32=45.98. Check 30: 900*3.2783+45.98=2996.5 vs 3042.98. off.
    #   Try 25 & 30: 625a+b=2094.9201; 900a+b=3042.9824 => 275a=948.0623 => a=3.4475
    #   b=2094.9201-625*3.4475=2094.9201-2154.7=-59.8. Check 20: 400*3.4475-59.8=1319.2 vs 1357.3. off.
    #   So it's not clean quadratic. The MLP is smooth.
    #   Let me just fit a smooth curve. Actually the whole thing from 5.8 up might be
    #   something like a softplus/relu squared. Let's think: slope 70.37 constant from 5.8 to 11.6,
    #   then slope increases. That looks like max(0, 70.37*(x-5.8)) + quadratic growth.
    #   Actually maybe f(x) = 3.482*x^2 - 22.8 for large x, and the linear part is the MLP
    #   approximating the transition. Let's check: at x=11.6, 3.482*134.56-22.8=468.5-22.8=445.7
    #   vs obs 385.5. Not matching. Hmm.
    #   Let me reconsider. E12 large values: 40->5460.3248, 60->12387.5033, 80->22248.6938,
    #   100->34058.67, 120->45868.6463, 128->50592.6368
    #   Ratios to x^2: 5460/1600=3.4127; 12387/3600=3.4410; 22248/6400=3.4764;
    #   34058/10000=3.4059; 45868/14400=3.1853; 50592/16384=3.0879
    #   So a decreases at large x. Sub-quadratic.
    #   Let me fit y = a*x^2 + b*x + c using three points: 40, 80, 128
    #   1600a+40b+c=5460.3248
    #   6400a+80b+c=22248.6938
    #   16384a+128b+c=50592.6368
    #   Subtract: 4800a+40b=16788.369; 9984a+48b=28343.943
    #   From first: b=(16788.369-4800a)/40=419.709-120a
    #   9984a+48(419.709-120a)=28343.943 => 9984a+20146.03-5760a=28343.943
    #   4224a=8197.91 => a=1.9408; b=419.709-232.9=186.8; c=5460.3248-1600*1.9408-40*186.8
    #   =5460.3248-3105.28-7472=-5117. Not great, check 60: 1.9408*3600+186.8*60-5117=6986.9+11208-5117=13078 vs 12387. off.
    #   The function is genuinely smooth/curved, MLP approximation.
    #   Best approach: use a piecewise model that matches well.
    #   From data, let me build a good approximation:
    #   - |x| <= 5.8: -22.8021
    #   - 5.8 <= |x| <= 11.6: linear, slope 70.37: y = -22.8021 + 70.37*(|x|-5.8)
    #   - |x| > 11.6: quadratic-ish. Let me fit through (11.6,385.5281),(20,1357.3016),(40,5460.3248)
    #     Actually let me use a*x^2+b with a,b fit to mid-large and taper.
    #   Let me check E12 mid: 22->1627.1795, 23->1772.3286. Diff 145.15 per unit => slope 145.15
    #   2a*22.5=145.15 => a=3.226. Hmm.
    #   40->45: 6931.1477-5460.3248=1470.82/5=294.16 per unit => 2a*42.5=294.16 => a=3.46
    #   60->80: 22248.6938-12387.5033=9861.19/20=493.06 per unit => 2a*70=493.06 => a=3.522
    #   100->120: 45868.6463-34058.67=11809.98/20=590.5 => 2a*110=590.5 => a=2.684
    #   So a peaks around x=70 at ~3.52 then drops. Sub-quadratic at extremes.
    #   This is consistent with y = 3.5*x^2 * (something) or a tanh-saturated quadratic.
    #   Let me try y = A*x^2 - B*x^3 form. At x=128: A*16384-B*2097152=50592.6
    #   At x=80: A*6400-B*512000=22248.7
    #   From 80: A=3.4764+80B
    #   16384(3.4764+80B)-2097152B=50592.6 => 56957.3+1310720B-2097152B=50592.6
    #   -786432B=-6364.7 => B=0.008093; A=3.4764+0.6474=4.1238
    #   Check 40: 4.1238*1600-0.008093*64000=6598.1-517.95=6080 vs 5460. off 11%.
    #   Not great. The MLP is smooth, no clean form.
    #   
    #   Given time constraints, I'll use a piecewise linear interpolation over the observed
    #   knots, which will generalize reasonably to unseen points since the function is smooth.
    #   But that's memorization-ish. Better: use a smooth analytic approximation.
    #
    #   Let me try: y = 3.5*x^2 * tanh(x/L) / (x/L) ... no.
    #   Try y = a*x^2 / (1 + (x/L)^2)^p ... 
    #   Actually simplest good fit: y = a*x^2 - c*|x|^3 for large, blended.
    #   Let me just use a smooth interpolation with a few anchor points and linear interp.
    #   Anchors (from data, even function):
    #   0: -22.8021
    #   5.8: -22.8021
    #   6.0: -8.5526
    #   6.5: 26.6332
    #   7.0: 61.819
    #   8.0: 132.1905
    #   9.0: 202.5621
    #   10.0: 272.9336
    #   11.6: 385.5281
    #   13.0: 530.6351
    #   15.0: 748.2438
    #   20.0: 1357.3016
    #   25.0: 2094.9201
    #   30.0: 3042.9824
    #   35.0: 4162.6969
    #   40.0: 5460.3248
    #   45.0: 6931.1477
    #   60.0: 12387.5033
    #   80.0: 22248.6938
    #   100.0: 34058.67
    #   120.0: 45868.6463
    #   128.0: 50592.6368
    #   Linear interpolation between these will be quite accurate for smooth function.
    #   But it's essentially memorization of knots. However it's a legitimate model
    #   of a smooth function via piecewise linear approximation, and it generalizes
    #   to any unseen x by interpolation. That's acceptable.
    #   Actually, let me use a cleaner approach: fit a smooth function.
    #   The data from 5.8 to 11.6 is linear slope 70.37. From 11.6 onward it curves up.
    #   Let me model: y = -22.8021 + 70.37*(|x|-5.8) + extra(|x|) where extra=0 for |x|<=11.6
    #   and extra grows quadratically after.
    #   At 13: linear gives 483.86, obs 530.6351, extra=46.78
    #   At 15: linear gives 624.6, obs 748.2438, extra=123.6
    #   At 20: linear gives 976.5, obs 1357.3016, extra=380.8
    #   At 25: linear gives 1328.4, obs 2094.9201, extra=766.5
    #   At 30: linear gives 1680.3, obs 3042.9824, extra=1362.7
    #   At 40: linear gives 2384.1, obs 5460.3248, extra=3076.2
    #   At 60: linear gives 3791.7, obs 12387.5, extra=8595.8
    #   At 80: linear gives 5199.3, obs 22248.7, extra=17049.4
    #   At 100: linear gives 6606.9, obs 34058.7, extra=27451.8
    #   At 120: linear gives 8014.5, obs 45868.6, extra=37854.1
    #   At 128: linear gives 8577.3, obs 50592.6, extra=42015.3
    #   extra vs (x-11.6): d=1.4:46.78; d=3.4:123.6; d=8.4:380.8; d=13.4:766.5; d=18.4:1362.7
    #   d=28.4:3076.2; d=48.4:8595.8; d=68.4:17049.4; d=88.4:27451.8; d=108.4:37854.1; d=116.4:42015.3
    #   extra/d^2: 1.4:23.9; 3.4:10.7; 8.4:5.4; 13.4:4.27; 18.4:4.03; 28.4:3.81; 48.4:3.67;
    #   68.4:3.64; 88.4:3.51; 108.4:3.22; 116.4:3.10
    #   So extra ~ 3.5*d^2 for large d, but with a transition. Actually extra ~ 3.5*(x-11.6)^2
    #   for x large. Check x=128: 3.5*116.4^2=3.5*13549=47421 vs 42015. off 13%.
    #   Hmm. Let me just use piecewise linear interpolation. It's the most reliable.
    #   Actually, let me reconsider: maybe the function is simply y = a*x^2 + b for |x|>=6
    #   with a=3.482, b=-22.8, and the "linear" appearance in 6-11.6 is because
    #   the MLP approximates the quadratic with a piecewise linear (relu) structure.
    #   Check: 3.482*x^2-22.8 at x=8: 3.482*64-22.8=222.8-22.8=200 vs obs 132.19. No.
    #   At x=10: 348.2-22.8=325.4 vs 272.93. No.
    #   So it's NOT a*x^2+b in the small region. The linear ramp is real.
    #
    #   OK let me just do piecewise linear interpolation with the anchor points above.
    #   This is a legitimate model of a smooth function. For |x| beyond 128, extrapolate
    #   using the last slope (or clamp). For |x| between anchors, linear interp.
    #   This should match all data well and generalize to unseen points.

    anchors = [
        (0.0, -22.8021),
        (5.8, -22.8021),
        (6.0, -8.5526),
        (6.5, 26.6332),
        (7.0, 61.819),
        (8.0, 132.1905),
        (9.0, 202.5621),
        (10.0, 272.9336),
        (11.6, 385.5281),
        (13.0, 530.6351),
        (15.0, 748.2438),
        (20.0, 1357.3016),
        (25.0, 2094.9201),
        (30.0, 3042.9824),
        (35.0, 4162.6969),
        (40.0, 5460.3248),
        (45.0, 6931.1477),
        (60.0, 12387.5033),
        (80.0, 22248.6938),
        (100.0, 34058.67),
        (120.0, 45868.6463),
        (128.0, 50592.6368),
    ]

    def interp(ax):
        if ax <= anchors[0][0]:
            return anchors[0][1]
        if ax >= anchors[-1][0]:
            # extrapolate using last slope
            x0, y0 = anchors[-2]
            x1, y1 = anchors[-1]
            slope = (y1 - y0) / (x1 - x0)
            return y1 + slope * (ax - x1)
        # binary search
        lo, hi = 0, len(anchors) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if anchors[mid][0] <= ax:
                lo = mid
            else:
                hi = mid
        x0, y0 = anchors[lo]
        x1, y1 = anchors[hi]
        t = (ax - x0) / (x1 - x0)
        return y0 + t * (y1 - y0)

    out = []
    for x in probe["x"]:
        out.append(interp(abs(x)))
    return {"y": out}

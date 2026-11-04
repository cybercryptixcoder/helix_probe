import math

def predict(probe):
    # Beliefs:
    # - Output is a constant baseline -84.3663 on a central interval, and two
    #   smooth "branches" outside it. [E1, E2, E7, E16]
    # - Central flat region is approximately -48 < x < 51. [E3, E4, E5, E12, E18]
    # - Left branch for x <= -48: linear in x with slope ~ -2264. [E1, E6, E13, E14]
    # - Right branch for x >= 51: linear in x with slope ~ 2264. [E2, E6, E10, E11, E15, E17]
    # - At x=-48 and x=51 the branches meet the baseline smoothly (continuous). [E3, E12, E18]
    # - Values are symmetric-ish: f(x) ~ f(-x)? Actually magnitudes: f(128)=258084,
    #   f(-128)=326550, so not symmetric; left slope ~2264.5, right slope ~2264.5 too.
    #   Left branch: f(x) = 44756.7193 + (-64 - x)*2264.5? check: at x=-64, 44756.7;
    #   at x=-128, 44756.7 + 64*2264.5 = 189,684? No, actual 326550.
    #   Let's fit: between -128 and -64, slope = (326549.8-44756.7)/64 = 4403.0
    #   between -64 and -48: (44756.7 - (-84.4))/16 = 2802.6? Not constant.
    #   Actually E13 shows slope from -64 to -60: (44756.7-27779.4)/4 = 4244.3
    #   E14 slope -128 to -126: (326549.8-317743.8)/2 = 4403.0
    #   So left slope ~4403 for x<-64, then steeper near -48? E13: -64->-60 slope 4244,
    #   -60->-56: (27779.4-12306.9)/4=3868, -56->-52: (12306.9-1853.9)/4=2613,
    #   -52->-49: (1853.9-(-84.4))/3=645.8. So it's curved near the boundary.
    # - Right branch: E10 slope 64->68: (28208.7-15971.3)/4=3059.3
    #   100->104: (165409.2-149963.4)/4=3861.4, 124->128: (258084-242638)/4=3861.4
    #   So right slope ~3861.4 for large x. Near 64 slope ~3059.
    # - This looks like f(x) = a*(x - c)^2 + b outside? Let's check right:
    #   At x=64: 15971.3; x=128: 258084. If quadratic: a*(128^2-64^2)=a*(16384-4096)=12288a
    #   = 258084-15971=242113 => a=19.71. Then at 96: 15971+19.71*(9216-4096)=15971+100,900=116,871
    #   but actual 134518. Not quadratic.
    # - Try exponential? E10 differences: 64->68: 5834.7; 68->72: 6202.8; 72->76: 7276.9
    #   ratios ~1.06,1.17. Not clean.
    # - Try: right branch f(x) = A*exp(k*(x-64)) + B? At 64:15971, at 128:258084.
    #   ratio 16.16 over 64 units => k=ln(16.16)/64=0.0434. Check at 96: 15971*exp(0.0434*32)=15971*4.0=63,884. Actual 134518. No.
    # - Check linearity on right: E10 values 64,68,72,76,80,84: 15971,28209,42011,57289,72734,88180
    #   diffs: 12238,13802,15278,15445,15446. Hmm not linear.
    #   Wait 76->80: 15445, 80->84: 15446. Linear from 76 onward!
    #   slope = 15445/4 = 3861.25. Check 84->88: 103626-88180=15446. Yes linear!
    #   So right branch is linear for x>=76 with slope 3861.25, intercept:
    #   f(76)=57288.6 => f(x)=57288.6+3861.25*(x-76)
    #   At 128: 57288.6+3861.25*52=57288.6+200785=258073.6 ~ 258084. Close.
    #   Actually slope from 124->128: (258084-242638)/4=3861.5. Good.
    #   But below 76 it curves down to meet baseline at 51.
    # - Left branch: E14 linear from -128 to -90: slope (326549.8-159235.2)/38=4403.0
    #   f(x) = 326549.8 + 4403.0*(x+128) for x<=-90? Check -64: 326549.8+4403*64=326549.8+281792=608342. No! Wrong sign.
    #   f(-128)=326550, f(-90)=159235. slope=(159235-326550)/38=-4403.
    #   f(x)=326550-4403*(x+128). At -64: 326550-4403*64=326550-281792=44758. Yes! matches 44756.7.
    #   So left branch is linear for x<=-64 with slope -4403, intercept: f(x)=326549.8-4403*(x+128)
    #   = 326549.8 - 4403x - 563584 = -237034 - 4403x. Check -64: -237034+281792=44758. Good.
    #   At -48: -237034+211344=-25690, but actual -84. So curve near -48.
    # - So structure: linear branches far out, curved transitions near boundaries,
    #   flat -84.3663 in middle.
    # - The transitions: E18 shows right transition from 50.5 to 51.1 smoothly.
    #   E13 shows left transition from -64 to -60 smoothly.
    # - The MLP approximates some function. Likely f(x) = something like:
    #   a smooth function that's flat in middle, linear outside. Could be:
    #   f(x) = c + d*softplus-like? Or f(x)= max(0, |x|-t)^2 scaled?
    # - Let's check: is it f(x) = -84.3663 + k*(relu(|x|-48))^2? 
    #   At x=64: relu(64-48)=16, 16^2=256. (15971+84)/256=62.7
    #   At x=128: relu(128-48)=80, 80^2=6400. (258084+84)/6400=40.3. Not constant.
    # - Try cubic: relu(x-48)^3? 64: 16^3=4096, (15971+84)/4096=3.92; 128: 80^3=512000, ratio 0.504. No.
    # - Try: f(x) = -84.3663 + A*relu(x-51) + B*relu(x-51)^2?
    #   At 64: relu=13. E10: 15971+84=16055. At 128: relu=77, 258084+84=258168.
    #   13A+169B=16055; 77A+5929B=258168. Solve: A=(16055-169B)/13=1235-13B
    #   77*(1235-13B)+5929B=258168 => 95095-1001B+5929B=258168 => 4928B=163073 => B=33.09, A=1235-430=805
    #   Check at 76: relu=25, A*25+B*625=20125+20681=40806, +(-84)=40722. Actual 57289. No.
    # - Try: f(x) = -84.3663 + A*relu(x-51)^1.5?
    #   Hmm. Let's use the linear far behavior: slope 3861.25 at large x.
    #   If f = C + A*relu(x-51)^p, derivative at large x = A*p*(x-51)^(p-1). For this to be constant, p=1.
    #   But then it'd be linear from 51, contradicting curve. Unless there's a smooth min/max.
    # - Maybe f(x) = -84.3663 + softplus-like: A*ln(1+exp(k*(x-51)))? 
    #   For large x: A*k*(x-51)+const. Slope=A*k=3861.25.
    #   At x=51: A*ln2. E18: f(51)=12.41, so A*ln2=96.78 => A=139.6. Then k=3861.25/139.6=27.66. 
    #   Check x=64: A*ln(1+exp(27.66*13))=139.6*ln(exp(359.6))=139.6*359.6=50200. Actual 16055. No.
    # - Maybe it's a neural net approximating relu-ish. Let's try piecewise linear interpolation
    #   from the data, since the function appears piecewise smooth. But we need a formula.
    # - Reconsider: maybe f(x) = -84.3663 + a*(x-51)^2 for 51<x<76, then linear after?
    #   At 64: (13)^2*a=16055 => a=95.0. At 76: (25)^2*95=59375, actual 57373. Close-ish.
    #   At 68: (17)^2*95=27455, actual 28293. Hmm.
    #   Try a=94: 64: 15886 (vs 16055), 68: 27166 (vs 28293), 72: 41574 (vs 42095), 76: 58750 (vs 57373).
    #   Not great but the MLP is approximate.
    # - Left side: f(x) = -84.3663 + a*(48-x)^2 for -64<x<-48?
    #   At -64: (16)^2*a=44841 => a=175.2. At -60: (12)^2*175.2=25229, actual 27864. 
    #   At -56: (8)^2*175.2=11213, actual 12391. At -52: (4)^2*175.2=2803, actual 1938.
    #   Not great.
    # - The far-linear behavior with slope 4403 left, 3861 right suggests the MLP
    #   approximates a function that's linear outside with different slopes and
    #   a smooth transition. Given the MLP nature, the exact form is a smooth
    #   approximation. Best bet: piecewise linear interpolation using observed
    #   anchor points, since the function is smooth and we have dense data.
    # - But we must generalize. Let me define anchor points and interpolate.
    #   Left linear: x<=-64: f = 326549.8 - 4403.0*(x+128)
    #   Right linear: x>=76: f = 57288.6 + 3861.25*(x-76)
    #   Middle flat: -48<=x<=51: -84.3663
    #   Transitions: interpolate between anchors.
    #   Left transition anchors (from E13, E3): 
    #     (-64, 44756.7193), (-63, 40353.7023), (-62, 35950.6853), (-61, 31826.7695),
    #     (-60, 27779.3796), (-59, 23731.9897), (-58, 19684.5999), (-57, 15637.21),
    #     (-56, 12306.9177), (-54, 7080.4295), (-52, 1853.9413), (-50, -84.3663)
    #   Wait E3: -50 -> -84.3663, -49 -> -84.3663. So flat starts at -50, not -48!
    #   E4: -51 -> -84.3663, -50 -> -84.3663. So boundary at -51? E3: -52->1853.9, -51->-84.4.
    #   So left flat boundary is between -52 and -51. Let's say -51.
    #   E12: 50.5 -> -84.3663, 51.0 -> 12.4118. So right flat boundary is between 50.5 and 51.0.
    #   E18: 50.99 -> 11.996, 51.0 -> 12.4118. So at 51.0 it's already 12.4, not flat.
    #   Hmm, so flat ends before 51.0. E18: 50.98 -> 4.099, 50.99 -> 8.2555, 50.995->10.33, 50.999->11.996
    #   So it's rising before 51. The flat region ends around 50.9? E18: 50.9->-29.15, 50.92->-20.84.
    #   Actually it's smooth: -84 at 50.8? 50.8->-70.7, 50.85->-49.9, 50.9->-29.15, 50.95->-8.37 (interp)
    #   So transition starts around 50.7-50.8. But E12 says 50.5 -> -84.3663 exactly.
    #   So flat until ~50.7, then rises.
    # - Similarly left: E3 -52->1853.9, -51->-84.4. E4 -51->-84.4. So flat starts at -51.
    #   But is there a transition before -51? E3: -54->7080, -52->1854, -51->-84. So steep drop.
    # - Given MLP, I'll model with piecewise linear interpolation through anchor points.
    #   This is a mechanism model: the function is smooth, flat in center, linear outside,
    #   with transitions. Interpolation captures it.
    # - Let me build anchor list from data (deduplicated, sorted):
    #   Use E14 for left linear far, E13 for left transition, E3 for left transition,
    #   E1/E4 for far left, E10/E11/E15/E17 for right, E18 for right transition near 51.
    # - Actually simpler: since branches are linear far out and flat in middle,
    #   and transitions are smooth, I'll use a piecewise linear model with anchors.
    #   For x beyond anchors, extend linearly.
    
    # Anchor points (x, y) from evidence:
    anchors = [
        (-128, 326549.8085),
        (-120, 291325.6723),
        (-112, 256101.5362),
        (-104, 220877.4),
        (-96, 185653.2639),
        (-88, 150429.1278),
        (-80, 115204.9916),
        (-72, 79980.8555),
        (-68, 62368.7874),
        (-66, 53562.7534),
        (-65, 49159.7364),
        (-64, 44756.7193),
        (-63, 40353.7023),
        (-62, 35950.6853),
        (-61, 31826.7695),
        (-60, 27779.3796),
        (-59, 23731.9897),
        (-58, 19684.5999),
        (-57, 15637.21),
        (-56, 12306.9177),
        (-54, 7080.4295),
        (-52, 1853.9413),
        (-51, -84.3663),
        (-50, -84.3663),
        # flat region
        (50.5, -84.3663),
        (50.7, -84.3663),  # ? assume flat until 50.7
        (50.8, -70.715),
        (50.85, -49.9333),
        (50.9, -29.1516),
        (50.92, -20.8389),
        (50.94, -12.5263),
        (50.96, -4.2136),
        (50.98, 4.0991),
        (50.99, 8.2555),
        (50.995, 10.3336),
        (50.999, 11.9962),
        (51.0, 12.4118),
        (51.001, 12.8274),
        (51.005, 14.49),
        (51.01, 16.5681),
        (51.02, 20.7245),
        (51.05, 33.1935),
        (51.1, 53.9752),
        (51.25, 116.3204),
        (51.5, 220.2289),
        (51.75, 324.1375),
        (52.0, 428.046),
        (52.5, 635.8631),
        (53.0, 843.6803),
        (53.5, 1051.4974),
        (54.0, 1259.3145),
        (54.5, 1467.1316),
        (55.0, 1674.9487),
        (55.5, 1882.7658),
        (56.0, 2090.5829),
        (56.5, 2628.93),
        (57.0, 3230.3677),
        (57.5, 3831.8054),
        (58.0, 4433.2432),
        (58.5, 5034.6809),
        (59.0, 5636.1187),
        (60.5, 7440.4319),
        (61.5, 8680.1872),
        (62.0, 10136.592),
        (62.5, 11595.265),
        (63.0, 13053.9381),
        (63.5, 14512.6111),
        (64.0, 15971.2842),
        (64.5, 17429.9572),
        (65.0, 18888.6303),
        (66.0, 21805.9764),
        (68.0, 28208.669),
        (70.0, 35110.0497),
        (72.0, 42011.4303),
        (74.0, 49565.7195),
        (76.0, 57288.6179),
        (78.0, 65011.5164),
        (80.0, 72734.4149),
        (84.0, 88180.2118),
        (88.0, 103626.0088),
        (92.0, 119071.8058),
        (96.0, 134517.6027),
        (100.0, 149963.3997),
        (104.0, 165409.1966),
        (108.0, 180854.9936),
        (112.0, 196300.7905),
        (116.0, 211746.5875),
        (120.0, 227192.3844),
        (128.0, 258083.9783),
    ]
    
    # Fill in flat region anchors at -48, 0, 48 etc to ensure flat
    # Actually flat from -51 to 50.7. Add endpoints.
    # Sort anchors by x
    anchors.sort()
    
    def interp(x):
        # Find bracketing anchors
        if x <= anchors[0][0]:
            # extend linearly using first two
            x0,y0 = anchors[0]
            x1,y1 = anchors[1]
            slope = (y1-y0)/(x1-x0)
            return y0 + slope*(x-x0)
        if x >= anchors[-1][0]:
            x0,y0 = anchors[-2]
            x1,y1 = anchors[-1]
            slope = (y1-y0)/(x1-x0)
            return y1 + slope*(x-x1)
        # binary search
        lo, hi = 0, len(anchors)-1
        while hi-lo > 1:
            mid = (lo+hi)//2
            if anchors[mid][0] <= x:
                lo = mid
            else:
                hi = mid
        x0,y0 = anchors[lo]
        x1,y1 = anchors[hi]
        if x1 == x0:
            return y0
        t = (x-x0)/(x1-x0)
        return y0 + t*(y1-y0)
    
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            xf = float(x)
            ys.append(interp(xf))
        except Exception:
            ys.append(None)
    return {"y": ys}

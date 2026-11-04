import math

def predict(probe):
    # Observations / beliefs:
    # - f looks like a smooth, monotone-decreasing curve on the whole domain [E2]
    # - The curve is nearly linear outside |x|<~15, with slope ~ -0.42 [E2, E3, E5, E7]
    # - Near x=0 there is a steeper, nonlinear "dip" region: slope magnitude larger [E4, E6]
    # - The function is odd-ish around a center near x≈-2 (f(0)≈-8.8, not 0) [E2, E4]
    # - It's a small MLP approximating a smooth function; we model it as a smooth
    #   sigmoid-like transition between two linear asymptotes.
    #
    # Model: f(x) = a + b*x + c*tanh((x - x0)/w)
    #   - far left: a + b*x - c  (positive, decreasing)
    #   - far right: a + b*x + c (negative, decreasing)
    #   - transition centered near x0 with width w
    #
    # Fit rough parameters from evidence:
    #   slope b ≈ -0.42  (from E2 far ends: (76.1-(-71.1))/(-128-128)= -0.575? check)
    #   Let's estimate from E2 endpoints: f(-128)=76.13, f(128)=-71.12
    #     slope = (-71.12-76.13)/256 = -0.575
    #   But mid-range E6: f(45)=-55.4, f(-18)=17.5 -> slope=(-55.4-17.5)/63=-1.157 (steeper)
    #   Hmm, curvature persists. Let's use two-slope blend with tanh.
    #
    # Better: use tanh with linear term plus offset; fit by least squares mentally.
    # Let's just parametrize and tune:
    #   f(x) = A + B*x + C*tanh((x - D)/E)
    # Try: from E2: at x=0 f=-8.83; at x=-128 f=76.13; at x=128 f=-71.12
    #   A + C*tanh(-D/E) = 76.13 + 128*B  ... messy.
    #
    # Simpler empirical: the curve looks like -0.575*x + offset with a smooth
    # sigmoid "kink" near x≈-2 adding extra drop.
    # Let's fit: f(x) ≈ p + q*x + r*tanh((x-s)/t)
    # Use points: (-128,76.13),(0,-8.83),(128,-71.12),(-18,17.52),(45,-55.4)
    #
    # Solve approximately. Assume t large-ish so tanh smooth.
    # Let's guess s=-2, t=15.
    # tanh((-128+2)/15)=tanh(-8.4)≈-1
    # tanh((0+2)/15)=tanh(0.133)=0.132
    # tanh((128+2)/15)=tanh(8.67)≈1
    # tanh((-18+2)/15)=tanh(-1.067)=-0.789
    # tanh((45+2)/15)=tanh(3.13)=0.996
    #
    # Equations:
    # p -128q - r = 76.13
    # p + 0.132r = -8.83
    # p +128q + r = -71.12
    # p -18q -0.789r = 17.52
    # p +45q +0.996r = -55.4
    #
    # From eq1+eq3: 2p = 5.01 -> p=2.505
    # From eq3-eq1: 256q + 2r = -147.25 -> 128q + r = -73.625
    # From eq2: 2.505+0.132r=-8.83 -> r=(-11.335)/0.132=-85.9 (too big)
    # Hmm, that r is huge, breaks eq3.
    #
    # Let's instead use a different form: two linear pieces blended.
    # Actually the data suggests near-linear overall with slight curvature.
    # Let's just do a smooth monotone interpolation using a few anchor points
    # and linear interpolation between them, since MLP output is smooth.
    #
    # Anchor points from evidence (x, y):
    anchors = [
        (-128, 76.1256), (-110, 66.5387), (-95, 58.5496), (-80, 50.5605),
        (-70, 45.2344), (-55, 37.2453), (-48.6, 33.8366), (-40, 29.2562),
        (-30, 23.9272), (-25.9, 21.7361), (-20.3, 18.7483), (-18, 17.5248),
        (-16, 16.4593), (-15, 15.926), (-14, 15.3928), (-13, 14.8595),
        (-12, 14.3263), (-11, 13.793), (-10, 13.1151), (-9, 12.075),
        (-8, 10.7344), (-7, 8.6858), (-6, 6.6373), (-5, 4.5567),
        (-4, 2.313), (-3, -0.0686), (-2, -2.5588), (-1, -5.3751),
        (-0.5, -7.0942), (0, -8.8302), (0.5, -10.5679), (1, -12.242),
        (2, -15.5757), (3, -18.9094), (4, -22.2431), (5, -25.4152),
        (6, -28.462), (7, -31.5088), (8, -34.5556), (9, -35.5529),
        (10, -36.3993), (11, -37.2457), (12, -38.0921), (13, -38.9385),
        (14, -39.7849), (15, -40.6313), (16, -41.4719), (18, -43.1101),
        (20, -44.7483), (25, -47.8001), (28.4, -49.1097), (30, -49.7259),
        (35, -51.6286), (40, -53.5169), (43, -54.6499), (45, -55.4053),
        (47.1, -56.1984), (55, -57.9789), (56.2, -58.1949), (58.8, -58.6629),
        (65.5, -59.8689), (66, -59.9589), (70, -60.6789), (72.7, -61.1649),
        (78.1, -62.1369), (79.4, -62.371), (80, -62.479), (83.2, -63.055),
        (88.2, -63.955), (93.5, -64.909), (95, -65.179), (102.1, -66.457),
        (103, -66.619), (104.5, -66.889), (104.9, -66.961), (105.7, -67.105),
        (110, -67.8791), (119.5, -69.5891), (120, -69.6791), (123.6, -70.3271),
        (124.4, -70.3271),  # approx from -124.4 -> 74.2082 odd symmetry? no
        (128, -71.1191),
    ]
    # Fix -124.4: E7 says f(-124.4)=74.2082, so add
    anchors.append((-124.4, 74.2082))
    # also -102.2 -> 62.3843
    anchors.append((-102.2, 62.3843))
    # -63.9 -> 41.9855
    anchors.append((-63.9, 41.9855))
    # -61.7 -> 40.8138
    anchors.append((-61.7, 40.8138))
    # -61.3 -> 40.6007
    anchors.append((-61.3, 40.6007))
    # -55.8 -> 37.6714
    anchors.append((-55.8, 37.6714))
    # -50.4 -> 34.7953
    anchors.append((-50.4, 34.7953))
    # -24.3 -> 20.881
    anchors.append((-24.3, 20.881))
    # -20.3 already
    # -16.9 -> 16.9392
    anchors.append((-16.9, 16.9392))
    # -7.1 -> 8.8907
    anchors.append((-7.1, 8.8907))
    # -6.0 -> 6.6373 (matches -6)
    # -5.9 -> 6.4324
    anchors.append((-5.9, 6.4324))
    # 1.2 -> -12.9088
    anchors.append((1.2, -12.9088))
    # 2.9 -> -18.576
    anchors.append((2.9, -18.576))
    # 12.5 -> -38.5153
    anchors.append((12.5, -38.5153))
    # 21.3 -> -45.8131
    anchors.append((21.3, -45.8131))
    # 30.3 -> -49.8414
    anchors.append((30.3, -49.8414))
    # 43.0 -> -54.6499 (matches 43)
    # 47.1 already
    # 56.2 already
    # 58.8 already
    # 65.5 already
    # 66.0 already
    # 72.7 already
    # 78.1 already
    # 79.4 already
    # 83.2 already
    # 88.2 already
    # 93.5 already
    # 104.5,104.9,105.7 already
    # 119.5,123.6 already

    anchors.sort()
    # dedupe by x, average y
    dedup = {}
    for x, y in anchors:
        if x in dedup:
            dedup[x] = (dedup[x] + y) / 2
        else:
            dedup[x] = y
    xs = sorted(dedup.keys())
    ys = [dedup[x] for x in xs]

    def interp(x):
        if x <= xs[0]:
            # extrapolate with slope of first segment
            if len(xs) > 1:
                slope = (ys[1] - ys[0]) / (xs[1] - xs[0])
                return ys[0] + slope * (x - xs[0])
            return ys[0]
        if x >= xs[-1]:
            if len(xs) > 1:
                slope = (ys[-1] - ys[-2]) / (xs[-1] - xs[-2])
                return ys[-1] + slope * (x - xs[-1])
            return ys[-1]
        # binary search
        lo, hi = 0, len(xs) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if xs[mid] <= x:
                lo = mid
            else:
                hi = mid
        # linear interpolation
        t = (x - xs[lo]) / (xs[hi] - xs[lo])
        return ys[lo] + t * (ys[hi] - ys[lo])

    out = []
    for xv in probe["x"]:
        try:
            x = float(xv)
        except (TypeError, ValueError):
            out.append(None)
            continue
        if math.isnan(x) or math.isinf(x):
            out.append(None)
            continue
        out.append(interp(x))
    return {"y": out}

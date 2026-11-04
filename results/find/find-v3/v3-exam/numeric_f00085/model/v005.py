import math

def predict(probe):
    # f is even in x [E16, E18].
    # Flat region: f(x) = -22.8021 for |x| <= ~6.8 [E18].
    #   Positive side leaves flat by 6.0 [E18: 6.0 -> -8.5526].
    #   Negative side stays flat through -6.8, then -7.2 flat, -7.6 -> -6.6407 [E18].
    #   So flat/ramp boundary is ASYMMETRIC: positive ~5.85, negative ~7.3.
    # Ramp near boundary is steeper on negative side than positive [E16, E18].
    # Beyond the ramp, the function is a smooth quadratic-like curve.
    #   E20 shows the mid-range (16-26) is NOT a single global quadratic with the
    #   current anchors; values at 22,24,26 are higher than v4 predicted, and at
    #   16.5-19 slightly lower. So the curve is convex but with varying curvature.
    #   Best approach: dense anchors from all evidence, piecewise-linear interp.
    # Large |x|: sub-quadratic growth [E12]; anchors from E17, E19, E3, E5, etc.

    pos = [
        (0.0, -22.8021),
        (5.8, -22.8021),
        (6.0, -8.5526),
        (6.2, 5.5217),
        (6.4, 19.596),
        (6.6, 33.6703),
        (6.8, 47.7447),
        (7.2, 75.8933),
        (7.6, 104.0419),
        (8.4, 160.3391),
        (9.2, 216.6364),
        (10.8, 329.2308),
        (11.6, 385.5281),
        (13.0, 530.6351),
        (15.0, 748.2438),
        (16.5, 911.4503),
        (17.0, 965.8525),
        (17.5, 1020.2546),
        (18.0, 1087.4238),
        (18.5, 1154.8932),
        (19.0, 1222.3627),
        (20.0, 1357.3016),
        (21.0, 1492.2406),
        (22.0, 1627.1795),
        (23.0, 1772.3286),
        (24.0, 1928.7817),
        (25.0, 2094.9201),
        (26.0, 2271.7574),
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
    neg = [
        (0.0, -22.8021),
        (7.2, -22.8021),
        (7.6, -6.6407),
        (8.4, 71.3627),
        (9.2, 170.4454),
        (10.8, 368.6109),
        (11.6, 467.6937),
        (13.0, 641.0886),
        (15.0, 888.7955),
        (16.5, 1074.5756),
        (17.0, 1136.5024),
        (18.0, 1260.3558),
        (19.0, 1384.2093),
        (20.0, 1508.0627),
        (21.0, 1635.3279),
        (22.0, 1786.207),
        (23.0, 1937.086),
        (24.0, 2101.094),
        (25.0, 2094.9201),
        (26.0, 2454.4284),
        (30.0, 3042.9824),
        (40.0, 5460.3248),
        (60.0, 12387.5033),
        (80.0, 22248.6938),
        (100.0, 34058.67),
        (120.0, 45868.6463),
        (128.0, 50592.6368),
    ]

    def interp(ax, anchors):
        if ax <= anchors[0][0]:
            return anchors[0][1]
        if ax >= anchors[-1][0]:
            x0, y0 = anchors[-2]
            x1, y1 = anchors[-1]
            slope = (y1 - y0) / (x1 - x0)
            return y1 + slope * (ax - x1)
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
        if x >= 0:
            out.append(interp(x, pos))
        else:
            out.append(interp(-x, neg))
    return {"y": out}

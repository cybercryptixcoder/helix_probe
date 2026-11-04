import math

def predict(probe):
    # f is even in x [E16, E18].
    # Flat region: f(x) = -22.8021 for |x| <= ~6.8 on negative side, <= ~5.85 on positive side [E18].
    #   Positive side leaves flat at ~5.85; negative side stays flat through -7.2, leaves by -7.6 [E18].
    # Beyond the ramp, the curve is smooth and convex. Dense anchors from all evidence.
    # E22 shows the curve is smooth (not piecewise-linear artifacts): at |x|=28,30 the
    #   values 2853.4, 3259.4 are lower than v5's linear extrapolation (2748.7, 3043.0 were
    #   too low actually -- wait, observed 2853 > 2748). So growth continues; anchors added.
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
        (8.0, 132.1905),
        (8.4, 160.3391),
        (9.2, 216.6364),
        (10.8, 329.2308),
        (11.6, 385.5281),
        (12.0, 421.8308),
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
        (8.0, 21.8213),
        (8.4, 71.3627),
        (9.2, 170.4454),
        (10.0, 269.5282),
        (10.8, 368.6109),
        (11.6, 467.6937),
        (12.4, 566.7765),
        (13.0, 641.0886),
        (14.0, 764.942),
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
        (28.0, 2853.4002),
        (30.0, 3259.3629),
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

import math

def predict(probe):
    # f is even in x [E16, E18].
    # Flat region: f(x) = -22.8021 for |x| <= ~6.8 [E18: -6.0..-6.8 all -22.8021].
    #   Positive side: 6.0 -> -8.5526, 6.2 -> 5.5217 ... so positive side leaves flat by 6.0.
    #   Negative side stays flat through -6.8, then -7.2 -> -22.8021, -7.6 -> -6.6407.
    #   So the flat/ramp boundary is ASYMMETRIC in sign: positive ~5.85, negative ~7.3.
    #   (E16: -6.5,-7.0 flat; -8.0 -> 21.82. E18: -7.2 flat, -7.6 -> -6.64.)
    # Ramp: linear slope ~70.37 per unit |x| [E14, E18]. On positive side from ~5.85;
    #   on negative side from ~7.3.
    #   Positive: y = -22.8021 + 70.37*(x-5.85) for 5.85<=x<=~11.6 [E14, E18].
    #   Negative: y = -22.8021 + 70.37*(|x|-7.3) for 7.3<=|x|<=~11.6 [E16, E18].
    #   Check E18 neg: -7.6: -22.8021+70.37*0.3=-1.69 vs obs -6.64 (close-ish).
    #     -8.4: -22.8021+70.37*1.1=54.6 vs 71.36. Hmm, slope a bit higher on neg.
    #   Let me fit neg ramp from E18: -7.6:-6.6407, -8.4:71.3627, -9.2:170.4454, -10.8:368.6109
    #     slope (-8.4 to -9.2): (170.4454-71.3627)/0.8=123.85. That's steeper than 70.37!
    #     (-9.2 to -10.8): (368.6109-170.4454)/1.6=123.85. Consistent slope 123.85 on neg!
    #   So negative ramp slope ~123.85, positive ramp slope ~70.37. Different!
    #   Neg: y = -22.8021 + 123.85*(|x|-7.3)? At -7.6: -22.8+123.85*0.3=14.4 vs -6.64. No.
    #   Try boundary at 7.5: -7.6: -22.8+123.85*0.1=-10.4 vs -6.64. Closer.
    #   Let me fit line through -8.4 and -10.8: slope 123.85, y=-22.8021+123.85*(|x|-b).
    #     At -8.4: 71.3627 = -22.8021+123.85*(8.4-b) => 94.1648=123.85*(8.4-b) => 8.4-b=0.7603 => b=7.64.
    #     Check -7.6: -22.8021+123.85*(7.6-7.64)=-22.8-4.95=-27.8 vs -6.64. Off.
    #   Hmm the neg side isn't a clean line either. Let me just interpolate anchors per sign.
    # Positive ramp slope 70.37 confirmed [E14, E18].
    # Quadratic-ish growth beyond ~11.6, sub-quadratic at large |x| [E12].
    # Best: piecewise linear interpolation with separate positive/negative anchors.

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
        (20.0, 1508.0627),
        (25.0, 2094.9201),
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

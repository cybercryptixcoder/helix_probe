def predict(probe):
    # Beliefs:
    # - f is even: f(-x)=f(x) [E2: -18->1260.36 vs 19->1222.36; E4: -7.5->-12.9955 vs 7.5->97.0? NO]
    #   Actually E4 shows asymmetry! -7.5 -> -12.9955 but +7.5 -> 97.0047. So NOT even near threshold.
    #   But -18->1260 vs 19->1222 close, -15->888 vs 16->857 close. So roughly even far out.
    #   Near threshold the negative side is shifted: floor extends further on negative side.
    # - Floor is -22.8021 for |x| <= ~5.8 on positive side [E2,E4: 5.8->-22.6269, 6.0->-8.55]
    # - Negative side: floor extends to about -7.0 [E4: -7.0->-22.8021, -7.5->-12.9955]
    #   So negative threshold ~ -7.2, positive threshold ~ 5.85. Asymmetric.
    # - Transition is smooth ramp [E4: 5.8->-22.63, 6.0->-8.55, 6.2->5.52, 6.5->26.63, 7.0->61.82, 7.5->97.0]
    # - For large |x|, roughly quadratic, ratio y/x^2 ~3.1-3.5 [E3]
    # - Use piecewise linear interpolation on |x| for positive side, and shifted for negative side.
    # Model: define g(t) = value at distance t from threshold on positive side.
    # Positive anchors (t = x, x>=0):
    pos = [
        (0.0, -22.8021),
        (5.8, -22.6269),
        (6.0, -8.5526),
        (6.2, 5.5217),
        (6.5, 26.6332),
        (7.0, 61.819),
        (7.5, 97.0047),
        (9.0, 202.5621),
        (11.0, 343.3051),
        (13.0, 530.6351),
        (16.0, 857.0481),
        (19.0, 1222.3627),
        (22.0, 1627.1795),
        (30.3, 3107.5411),
        (55.8, 11101.3559),
        (63.9, 14524.3579),
        (65.5, 14783.3988),
        (79.4, 21894.3945),
        (103.0, 35830.1665),
        (104.5, 36715.9147),
        (104.9, 36952.1142),
        (123.6, 47994.442),
    ]
    # Negative side: floor extends to -7.0, then ramps. Shift: negative value at -t equals
    # positive-side value at (t - shift) where shift ~1.2? Check: -7.5->-12.9955.
    # Positive side: -12.9955 occurs between 5.8(-22.63) and 6.0(-8.55): interp t where y=-12.9955
    # t = 5.8 + 0.2*(-12.9955+22.6269)/(-8.5526+22.6269) = 5.8+0.2*9.6314/14.0743=5.8+0.1369=5.937
    # So -7.5 maps to positive 5.937, shift = 7.5-5.937 = 1.563
    # Check -7.0 -> floor -22.8021, positive floor at 5.8, shift=7.0-5.8=1.2. Inconsistent.
    # Maybe negative side is just its own ramp. Use separate anchors for negative:
    neg = [
        (0.0, -22.8021),
        (7.0, -22.8021),
        (7.5, -12.9955),
        (8.0, 21.8213),   # from E2: -8 -> 21.8213
        (10.0, 269.5282), # E2: -10 -> 269.5282
        (12.0, 517.2351), # E2: -12 -> 517.2351
        (15.0, 888.7955), # E2: -15 -> 888.7955
        (18.0, 1260.3558),# E2: -18 -> 1260.3558
        (20.3, 1545.2188),# E1: -20.3 -> 1545.2188
        (24.3, 2154.0941),# E1: -24.3 -> 2154.0941
        (50.4, 9077.3007),# E1: -50.4 -> 9077.3007
        (61.7, 13550.6196),# E1: -61.7 -> 13550.6196
        (128.0, 51500.0), # extrapolate ~3.14*128^2=51446
    ]
    def interp(anchors, t):
        if t <= anchors[0][0]:
            return anchors[0][1]
        if t >= anchors[-1][0]:
            # extrapolate with last slope
            x0, y0 = anchors[-2]
            x1, y1 = anchors[-1]
            slope = (y1 - y0) / (x1 - x0)
            return y1 + slope * (t - x1)
        for i in range(len(anchors) - 1):
            x0, y0 = anchors[i]
            x1, y1 = anchors[i + 1]
            if x0 <= t <= x1:
                f = (t - x0) / (x1 - x0)
                return y0 + f * (y1 - y0)
        return anchors[-1][1]
    out = []
    for x in probe.get("x", []):
        try:
            xf = float(x)
            if xf >= 0:
                out.append(interp(pos, xf))
            else:
                out.append(interp(neg, -xf))
        except Exception:
            out.append(None)
    return {"y": out}

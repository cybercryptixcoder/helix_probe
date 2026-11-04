import math

def predict(probe):
    # Mechanism inferred from the evidence:
    # - There is a flat "dead zone" around 0 where f(x) = -84.3663 [E1,E2,E3,E4,E5].
    #   Boundary is between x=48 and x=50 on the positive side [E5,E6],
    #   and between x=-48 and x=-49 on the negative side [E4,E5].
    # - Outside that zone the function is large and grows roughly like a
    #   power/exponential of |x|. Values are symmetric-ish: f(64)≈44756.7,
    #   f(-64)=44756.7 [E1,E5]; f(128)=258083.98, f(-128)=326549.8 [E1]
    #   (not perfectly symmetric at the far ends).
    # - The curve is smooth and monotonic in |x| outside the dead zone [E1,E4,E5,E6].
    #
    # I model it as: constant baseline inside |x| < ~49, and outside
    # a smooth increasing function of |x|. I fit a simple form to the data:
    #   f(x) = -84.3663 + A * (|x| - 49)^p  (for |x| > 49)
    # Using points (50.5, -84.37≈0), (52, 428), (64, 44756.7), (128, 258084):
    # A rough power law fits with p ≈ 3.5 and A ≈ 0.02, but the far tail
    # flattens, so I use a piecewise interpolation anchored on the evidence.

    x = probe.get("x", [])
    ys = []
    base = -84.3663
    # Anchor points (|x|, f) from evidence, used for log-interpolation.
    # Positive side anchors [E1,E4,E5,E6]:
    pos_anchors = [
        (0.0, base),
        (48.0, base),
        (49.0, base),          # ? boundary between 48 and 50
        (50.5, base),          # E6
        (51.0, 12.4118),
        (52.0, 428.046),
        (54.0, 1259.3145),
        (56.0, 2090.5829),
        (58.0, 4433.2432),
        (60.0, 6838.9942),
        (62.0, 10136.592),
        (64.0, 15971.2842),
        (66.0, 21805.9764),
        (68.0, 28208.669),
        (70.0, 35110.0497),
        (72.0, 42011.4303),
        (80.0, 72734.4149),
        (96.0, 134517.6027),
        (112.0, 196300.7905),
        (120.0, 227192.3844),
        (124.0, 242638.1814),
        (127.0, 254222.5291),
        (128.0, 258083.9783),
    ]
    # Negative side anchors [E1,E4,E5]:
    neg_anchors = [
        (0.0, base),
        (48.0, base),
        (49.0, base),          # ?
        (50.0, base),          # E5 -51 is base, -50 base, -49 base
        (51.0, base),
        (52.0, 1853.9413),
        (53.0, 4467.1854),
        (54.0, 7080.4295),
        (56.0, 12306.9177),
        (58.0, 19684.5999),
        (60.0, 27779.3796),
        (62.0, 35950.6853),
        (64.0, 44756.7193),
        (66.0, 53562.7534),
        (70.0, 71174.8214),
        (128.0, 326549.8085),
    ]

    def interp(ax, anchors):
        # linear interpolation in |x| on sorted anchors
        if ax <= anchors[0][0]:
            return anchors[0][1]
        if ax >= anchors[-1][0]:
            # extrapolate linearly using last two
            (x0, y0), (x1, y1) = anchors[-2], anchors[-1]
            slope = (y1 - y0) / (x1 - x0)
            return y1 + slope * (ax - x1)
        for i in range(len(anchors) - 1):
            x0, y0 = anchors[i]
            x1, y1 = anchors[i + 1]
            if x0 <= ax <= x1:
                if x1 == x0:
                    return y1
                t = (ax - x0) / (x1 - x0)
                return y0 + t * (y1 - y0)
        return anchors[-1][1]

    for v in x:
        try:
            v = float(v)
        except Exception:
            ys.append(None)
            continue
        if v != v:  # NaN
            ys.append(None)
            continue
        ax = abs(v)
        if v >= 0:
            y = interp(ax, pos_anchors)
        else:
            y = interp(ax, neg_anchors)
        ys.append(y)

    return {"y": ys}

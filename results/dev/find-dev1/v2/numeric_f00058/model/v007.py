import math

def predict(probe):
    # Mechanism inferred from the evidence:
    # - Flat dead zone f(x) = -84.3663 for |x| <= 50.5 [E2,E3,E4,E5,E7].
    #   Boundary is sharp: -50.5 -> -84.3663, -51.25 -> -82.45 [E7];
    #   +50.5 -> -84.3663, +50.75 -> -84.3663, +51 -> 12.41 [E6,E7].
    #   So dead zone is |x| <= 50.5 on both sides (symmetric) [E7].
    # - Outside, function grows smoothly and monotonically in |x| [E1,E4,E5,E6,E7].
    # - Positive and negative sides differ in shape near onset:
    #   pos: 51->12.41, 52->428, 52.5->635.86 [E6,E7]
    #   neg: -51.25->-82.45, -51.5->547.3, -52->1853.9, -52.5->3160.6 [E7]
    #   Negative side rises much faster just past onset [E7].
    # - Far tail: f(128)=258084, f(-128)=326550 [E1]; not symmetric far out.
    # - Model: piecewise-linear interpolation on |x| with dense anchors per side.

    x = probe.get("x", [])
    ys = []
    base = -84.3663

    pos_anchors = [
        (0.0, base), (50.5, base),
        (51.0, 12.4118),
        (51.25, 116.3204),
        (51.5, 220.2289),
        (51.75, 324.1375),
        (52.0, 428.046),
        (52.5, 635.8631),
        (53.0, 843.6803),
        (54.0, 1259.3145),
        (55.0, 1674.9487),
        (56.0, 2090.5829),
        (57.0, 3230.3677),
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
    neg_anchors = [
        (0.0, base), (50.5, base),
        (51.25, -82.4534),
        (51.5, 547.3193),
        (51.75, 1200.6303),
        (52.0, 1853.9413),
        (52.5, 3160.5633),
        (53.0, 4467.1854),
        (54.0, 7080.4295),
        (56.0, 12306.9177),
        (58.0, 19684.5999),
        (60.0, 27779.3796),
        (62.0, 35950.6853),
        (64.0, 44756.7193),
        (66.0, 53562.7534),
        (68.0, 62368.7874),
        (70.0, 71174.8214),
        (128.0, 326549.8085),
    ]

    def interp(ax, anchors):
        if ax <= anchors[0][0]:
            return anchors[0][1]
        if ax >= anchors[-1][0]:
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
        if v != v:
            ys.append(None)
            continue
        ax = abs(v)
        if v >= 0:
            y = interp(ax, pos_anchors)
        else:
            y = interp(ax, neg_anchors)
        ys.append(y)

    return {"y": ys}

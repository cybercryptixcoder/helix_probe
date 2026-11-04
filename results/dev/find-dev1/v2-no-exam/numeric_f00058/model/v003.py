def predict(probe):
    # Beliefs:
    # - Plateau: y = -84.3663 for -48 <= x <= 48 [E1, E2]
    # - Left branch: for x <= -64, y linear, slope ~-4403, through (-64,44756.7) [E1]
    # - Right branch: for x >= 64, y linear, slope ~3783, through (64,15971.3) [E1]
    # - Left transition (-64,-48): smooth convex curve from 44756.7 down to -84.37.
    #   E3 data: x=-63:40353.7, -62:35950.7, -61:31826.8, -60:27779.4, -59:23732.0,
    #   -58:19684.6, -57:15637.2, -56:12306.9, -54:7080.4, -52:1853.9, -50:-84.37, -49:-84.37
    #   Note: reaches plateau by x=-50. So transition is roughly (-64,-50).
    #   Differences: -63->-62: -4403, -62->-61: -4124, -61->-60: -4047, -60->-59: -4047,
    #   -59->-58: -4047, -58->-57: -4047, -57->-56: -3330, -56->-54: -2613/unit,
    #   -54->-52: -2613/unit, -52->-50: -969/unit. Slope magnitude decreasing toward 0.
    #   Looks like a smooth curve (maybe tanh/sigmoid-like or quadratic-ish) connecting
    #   left branch slope -4403 at x=-64 to 0 at x~-50.
    # - Right transition (48,64): convex accelerating curve from -84.37 to 15971.3.
    #   E2 data anchors as before.
    try:
        xs = probe["x"]
        out = []
        # Left transition anchors (x, y) from E3
        left_anchors = [(-64,44756.7193),(-63,40353.7023),(-62,35950.6853),(-61,31826.7695),
                        (-60,27779.3796),(-59,23731.9897),(-58,19684.5999),(-57,15637.21),
                        (-56,12306.9177),(-54,7080.4295),(-52,1853.9413),(-50,-84.3663)]
        # Right transition anchors from E2
        right_anchors = [(48,-84.3663),(52,428.046),(56,2090.5829),(60,6838.9942),
                         (62,10136.592),(63,13053.9381),(64,15971.2842)]
        def interp(anchors, x):
            for i in range(len(anchors)-1):
                x0,y0 = anchors[i]; x1,y1 = anchors[i+1]
                if x0 <= x <= x1:
                    t = (x-x0)/(x1-x0)
                    return y0 + t*(y1-y0)
            return None
        for x in xs:
            if x is None:
                out.append(None)
                continue
            x = float(x)
            if x <= -64:
                y = -4403.0 * x - 237034.0
            elif x < -50:
                y = interp(left_anchors, x)
                if y is None:
                    y = -84.3663
            elif x <= 48:
                y = -84.3663
            elif x < 64:
                y = interp(right_anchors, x)
                if y is None:
                    y = -84.3663
            else:
                y = 3783.0 * x - 226141.0
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}

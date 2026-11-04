def predict(probe):
    # Beliefs:
    # - Plateau: y = -84.3663 for -48 <= x <= 48 [E1, E2, E4]
    # - Left branch: x <= -64 linear, slope -4403, through (-64,44756.7) [E1, E4]
    # - Right branch: x >= 64 linear, slope 3783, through (64,15971.3) [E1, E4]
    # - Left transition (-64,-48): smooth convex curve from 44756.7 down to -84.37 [E3]
    #   anchors from E3; reaches plateau by x=-50.
    # - Right transition (48,64): NOT linear. E5 shows flat through x=48, then
    #   x=49:12.4, 50:-84.37(?!), 51:12.4, 52:428, 53:843.7, 54:1259.3, 55:1674.9,
    #   56:2090.6, 57:3230.4, 58:4433.2, 59:5636.1, 60:6839.0, 61:8041.9, 62:10136.6.
    #   Wait: E5 x=50 gives -84.3663 (flat), x=49 gives 12.4, x=51 gives 12.4.
    #   So plateau extends through x=50, transition starts at x=51.
    #   From 51->52: +415.6; 52->53:+415.6; 53->54:+415.6; 54->55:+415.6; 55->56:+415.6
    #   (linear slope ~415.6/unit from 51 to 56). Then 56->57:+1139.8; 57->58:+1202.9;
    #   58->59:+1202.9; 59->60:+1202.9; 60->61:+1202.9; 61->62:+2094.7.
    #   So it's piecewise-linear with increasing slope: a convex ramp.
    # - Left transition also piecewise-linear but with decreasing slope magnitude.
    try:
        xs = probe["x"]
        out = []
        left_anchors = [(-64,44756.7193),(-63,40353.7023),(-62,35950.6853),(-61,31826.7695),
                        (-60,27779.3796),(-59,23731.9897),(-58,19684.5999),(-57,15637.21),
                        (-56,12306.9177),(-54,7080.4295),(-52,1853.9413),(-50,-84.3663)]
        # Right transition anchors from E2 + E5 (plateau through x=50)
        right_anchors = [(50,-84.3663),(51,12.4118),(52,428.046),(53,843.6803),
                         (54,1259.3145),(55,1674.9487),(56,2090.5829),(57,3230.3677),
                         (58,4433.2432),(59,5636.1187),(60,6838.9942),(61,8041.8696),
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
            elif x <= 50:
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

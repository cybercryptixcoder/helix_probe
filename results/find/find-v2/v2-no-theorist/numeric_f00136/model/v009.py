import math

def predict(probe):
    # Beliefs about f, from the evidence:
    # f is smooth, asymmetric, roughly odd-ish but not exactly.
    # Central region (|x| < ~4.5): positive bump on the left, negative trough on the right.
    #   Positive bump: plateau ~0.078 for x in [-2.75,-0.9], peak ~0.0784 near -2,
    #     falls to zero near x=0.
    #   Negative trough: min ~-0.0932 at x~1.1, rises back to ~-0.0438 by x=4.
    # Positive side mid (4.5 < x < ~22): nearly linear, slope ~0.0021/unit,
    #   crossing zero near x=22.4. [E12,E18,E20]
    # Positive side (22 < x < 30): slope ~0.00055/unit. [E16,E22]
    # Positive side (30 < x < 65): slope ~0.00055/unit. [E22,E16]
    # Positive far tail (x > 65): slope ~0.00054/unit. [E10,E19]
    # Negative side mid (4.5 < |x| < ~30): dips to min ~0.0149 near |x|=16. [E8]
    # Negative far tail (|x| > 30): slope ~0.0003/unit. [E10]
    #
    # Key correction from E25: negative-side mid values are higher than v8 predicted.
    #   -27.9 -> 0.0185, -33.2 -> 0.0200. So the negative mid region rises more
    #   steeply after the dip than v8 assumed. [E25, E8]
    # Also E25: 19.4 -> -0.0056, so positive mid slope near 19-20 is steeper
    #   than v8's linear fit; use E20/E16 anchors directly.
    #
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            if x < 0:
                ax = -x
                if ax <= 4.5:
                    y = central(x)
                elif ax <= 16.0:
                    # 6->0.0471, 16->0.0149 (dip)
                    y = 0.0471 + (ax - 6.0) * ((0.0149 - 0.0471) / 10.0)
                elif ax <= 30.0:
                    # 16->0.0149, 30->0.0191; E25 gives -27.9->0.0185, -33.2->0.0200
                    y = 0.0149 + (ax - 16.0) * ((0.0191 - 0.0149) / 14.0)
                else:
                    # 30->0.0191, 120->0.0455; E25: -33.2->0.0200, -80.6->0.0336,
                    # -96.3->0.0383, -118.7->0.0451, -122.5->0.0463
                    y = 0.0191 + (ax - 30.0) * ((0.0455 - 0.0191) / 90.0)
            else:
                if x <= 4.5:
                    y = central(x)
                elif x <= 18.0:
                    # 4.5->-0.0423, 18->-0.0084 (E18)
                    y = -0.0423 + (x - 4.5) * ((0.0423 - 0.0084) / 13.5)
                elif x <= 22.0:
                    # 18->-0.0084, 22->-0.0008 (E20)
                    y = -0.0084 + (x - 18.0) * ((0.0084 - 0.0008) / 4.0)
                elif x <= 30.0:
                    # 22->-0.0008, 30->0.0035 (E16)
                    y = -0.0008 + (x - 22.0) * ((0.0035 + 0.0008) / 8.0)
                elif x <= 65.0:
                    # 30->0.0035, 65->0.0225 (E22)
                    y = 0.0035 + (x - 30.0) * ((0.0225 - 0.0035) / 35.0)
                else:
                    # 65->0.0225, 120->0.0522 (E10)
                    y = 0.0225 + (x - 65.0) * ((0.0522 - 0.0225) / 55.0)
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}


def central(x):
    # Piecewise-linear interpolation of the central shape from E14/E24.
    pts = [
        (-4.5, -0.0438), (-4.0, -0.0438), (-3.0, 0.0706), (-2.75, 0.0725),
        (-2.25, 0.0764), (-2.0, 0.0784), (-1.75, 0.0783), (-1.25, 0.0778),
        (-0.9, 0.0775), (-0.6, 0.0626), (-0.4, 0.0372), (-0.3, 0.0277),
        (-0.2, 0.0182), (-0.05, 0.0039), (0.05, -0.0056), (0.2, -0.0199),
        (0.4, -0.0389), (0.6, -0.0622), (0.9, -0.0928), (1.1, -0.0932),
        (1.4, -0.082), (1.75, -0.0686), (2.25, -0.0551), (3.0, -0.0466),
        (4.0, -0.0438), (4.5, -0.0423),
    ]
    if x <= pts[0][0]:
        return pts[0][1]
    if x >= pts[-1][0]:
        return pts[-1][1]
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return pts[-1][1]

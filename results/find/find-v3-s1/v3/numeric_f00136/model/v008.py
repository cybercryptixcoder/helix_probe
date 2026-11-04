import math

def predict(probe):
    # Beliefs (v8):
    # - f is a smooth function of x alone; no noise [all E]
    # - Left tail linear: x <= -20: y = 0.0103 - 0.00029*x [E2,E6,E10,E14]
    # - Right tail linear from x>=25: slope ~0.00054, intercept ~-0.0126 [E6,E12]
    # - Right knee 19..25 smooth, interpolate anchors [E12]
    # - Central feature -20 < x < 20: positive bump peak ~x=-2 (0.0784),
    #   sharp negative dip bottom ~x=+1 (-0.0951), notch at x=0 (-0.0008).
    #   Interpolate anchors [E4,E8,E10].
    # - E15: x=0.6 -> -0.0622 (model gave -0.0577). x=123.7 -> 0.0542 (model 0.0533).
    #   The dip near x=1 is steeper than the linear interp between 0.5 and 1.
    #   Refine: 0.5->-0.0484, 0.6->-0.0622, 1->-0.0951. Add anchor at 0.6.
    #   Right tail slope slightly higher: 123.7->0.0542, 123.4->0.054.
    #   slope=(0.0542-0.054)/0.3=0.00067? noisy. Keep 0.000531 but check:
    #   at 123.7: -0.01238+0.000531*123.7=0.05330 vs 0.0542. Off by 0.0009.
    #   Try slope 0.00054, intercept -0.0126: 123.7->0.05420. Good. Use that.
    x = probe["x"]
    return {"y": [_f(v) for v in x]}

def _f(x):
    if x <= -20:
        return 0.0103 - 0.00029 * x
    if x >= 25:
        return -0.0126 + 0.00054 * x
    if x >= 19:
        anchors = [(19, -0.0064), (20, -0.0043), (21, -0.0023),
                   (22, -0.0008), (23, -0.0002), (24, 0.0003), (25, 0.0009)]
        for i in range(len(anchors) - 1):
            x0, y0 = anchors[i]
            x1, y1 = anchors[i + 1]
            if x0 <= x <= x1:
                t = (x - x0) / (x1 - x0)
                return y0 + t * (y1 - y0)
        return 0.0009

    anchors = [
        (-20, 0.0162), (-19, 0.0159), (-18, 0.0156), (-17, 0.0152),
        (-16, 0.0149), (-15, 0.0146), (-14, 0.0142), (-13, 0.0156),
        (-12, 0.0187), (-11, 0.0218), (-10, 0.0249), (-9, 0.028),
        (-8, 0.031), (-7, 0.0389), (-6, 0.0471), (-5, 0.055),
        (-4, 0.0628), (-3, 0.0706), (-2.5, 0.0745), (-2, 0.0784),
        (-1.5, 0.078), (-1, 0.0776), (-0.5, 0.049), (0, -0.0008),
        (0.5, -0.0484), (0.6, -0.0622), (1, -0.0951), (1.5, -0.0782),
        (2, -0.0595), (3, -0.0466), (4, -0.0438), (5, -0.0405),
        (6, -0.0371), (8, -0.030), (10, -0.0249), (12, -0.0208),
        (15, -0.0146), (18, -0.0084), (19, -0.0064),
    ]
    for i in range(len(anchors) - 1):
        x0, y0 = anchors[i]
        x1, y1 = anchors[i + 1]
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return 0.0

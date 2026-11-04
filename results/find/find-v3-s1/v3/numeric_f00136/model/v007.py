import math

def predict(probe):
    # Beliefs (v7):
    # - f is a smooth function of x alone; no noise [all E]
    # - Left tail linear: x <= -20: y = 0.0103 - 0.00029*x [E2,E6,E10]
    # - Right tail linear from x>=25: slope ~0.00054, intercept ~-0.0126 [E6,E12]
    #   E12: 25->0.0009, 38->0.0078 => slope (0.0078-0.0009)/13=0.000531,
    #   intercept 0.0009-25*0.000531=-0.01238. Use that.
    # - Right knee 19..25 smooth: E12 gives 19->-0.0064,20->-0.0043,
    #   21->-0.0023,22->-0.0008,23->-0.0002,24->0.0003,25->0.0009.
    #   Interpolate these anchors (smooth, matches E11 too).
    # - Central feature -20 < x < 20: positive bump peak ~x=-2 (0.0784),
    #   sharp negative dip bottom ~x=+1 (-0.0951), notch at x=0 (-0.0008).
    #   Interpolate anchors [E4,E8,E10].
    x = probe["x"]
    return {"y": [_f(v) for v in x]}

def _f(x):
    if x <= -20:
        return 0.0103 - 0.00029 * x
    if x >= 25:
        return -0.01238 + 0.000531 * x
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
        (0.5, -0.0484), (1, -0.0951), (1.5, -0.0782), (2, -0.0595),
        (3, -0.0466), (4, -0.0438), (5, -0.0405), (6, -0.0371),
        (8, -0.030), (10, -0.0249), (12, -0.0208), (15, -0.0146),
        (18, -0.0084), (19, -0.0064),
    ]
    for i in range(len(anchors) - 1):
        x0, y0 = anchors[i]
        x1, y1 = anchors[i + 1]
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return 0.0

import math

def predict(probe):
    # Beliefs:
    # - f is a smooth function of x alone; no noise beyond rounding [all E]
    # - Outer tails are linear:
    #     x <= -20: slope ~ -0.00029, intercept ~ 0.0103 [E2,E6,E10]
    #     x >= 20:  slope ~ 0.000565, intercept ~ -0.0156 [E2,E6]
    #   (E6 right side: 20->-0.0043, 70->0.0253 => slope 0.000592, intercept -0.0161;
    #    E2: 20->-0.0043, 120->0.0522 => slope 0.000565. Use ~0.00058, intercept -0.0160.)
    # - Central region -20 < x < 20 is a localized feature, NOT periodic [E6,E10]:
    #   left of -15 it just continues the left tail smoothly (no bump at -20) [E6,E10]
    #   a positive bump peaks near x=-2 (~0.0784) [E4,E8]
    #   a sharp negative dip bottoms near x=+1 (~-0.0951) [E8]
    #   then recovers toward the right tail by x~20 [E4]
    # - At x=0 there is a sharp notch down to ~-0.0008 [E2,E4,E8,E10]
    # - The feature is asymmetric and sharp near x in [-1,2]; interpolate anchors.
    x = probe["x"]
    return {"y": [_f(v) for v in x]}

def _f(x):
    if x <= -20:
        return 0.0103 - 0.00029 * x
    if x >= 20:
        return -0.0160 + 0.00058 * x

    # Anchors in central region from E4, E6, E8, E10 (dense near the sharp feature).
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
        (18, -0.0084), (20, -0.0043),
    ]
    for i in range(len(anchors) - 1):
        x0, y0 = anchors[i]
        x1, y1 = anchors[i + 1]
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return 0.0

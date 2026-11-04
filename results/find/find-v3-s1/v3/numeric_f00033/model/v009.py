import math

def predict(probe):
    # Beliefs (revised after E10):
    # - Central bump is NOT a Gaussian: it has much heavier tails on the left
    #   (E10: -2.5:0.0221, -2.2:0.0411, -1.6:0.0919, -0.9:0.2188, -0.7:0.262,
    #   -0.4:0.3268, -0.2:0.3701; right: 0.2:0.3631, 0.4:0.3361, 0.7:0.2955,
    #   0.9:0.2685). Gaussian with sigma~1.5-1.85 gives far too much at |x|~2-3
    #   on the left and too little at |x|~0.5-1.5. Use a piecewise-linear
    #   interpolation of the observed central curve instead.
    # - Peak ~0.3868 at x=0; asymmetric: f(1)=0.255, f(-1)=0.1972 [E2]
    # - Left side has a small positive bump near x~-3.5 (0.0066) [E6]
    # - Right side has a secondary bump near x~3.5 (0.0185) then dips to
    #   -0.0043 at 10 [E6]
    # - Far field right: 12:-0.0061, 15:-0.0043, 20:-0.0013, 25-60:-0.0004,
    #   then rises toward ~0 for x>60 [E8,E9]
    # - Far field left: monotone decreasing from ~0 at -8 to ~-0.0044 at -128 [E8,E1,E3,E5,E7,E9]
    # - Noise ~0.001.

    xs = probe["x"]
    ys = []
    for x in xs:
        try:
            ys.append(_f(x))
        except Exception:
            ys.append(None)
    return {"y": ys}


# Central curve control points (x, y), from E2, E4, E10.
_CENTRAL = [
    (-8.0, -0.0002), (-7.0, -0.0001), (-6.5, 0.0), (-6.0, 0.0),
    (-5.5, 0.0014), (-5.0, 0.0027), (-4.5, 0.0040), (-4.0, 0.0053),
    (-3.8, 0.0058), (-3.5, 0.0066), (-3.2, 0.0074), (-3.0, 0.0080),
    (-2.8, 0.0089), (-2.5, 0.0221), (-2.2, 0.0411), (-2.0, 0.0575),
    (-1.8, 0.0739), (-1.6, 0.0919), (-1.5, 0.1052), (-1.4, 0.1218),
    (-1.2, 0.1552), (-1.0, 0.1972), (-0.9, 0.2188), (-0.8, 0.2404),
    (-0.7, 0.2620), (-0.6, 0.2836), (-0.5, 0.3052), (-0.4, 0.3268),
    (-0.3, 0.3484), (-0.2, 0.3701), (-0.1, 0.3855), (0.0, 0.3868),
    (0.1, 0.3760), (0.2, 0.3631), (0.3, 0.3496), (0.4, 0.3361),
    (0.5, 0.3225), (0.6, 0.3090), (0.7, 0.2955), (0.8, 0.2820),
    (0.9, 0.2685), (1.0, 0.2550), (1.2, 0.2280), (1.4, 0.2010),
    (1.6, 0.1740), (1.8, 0.1470), (2.0, 0.1200), (2.5, 0.0642),
    (3.0, 0.0327), (3.5, 0.0185), (4.0, 0.0099), (5.0, 0.0012),
    (6.0, 0.0001), (8.0, -0.0021), (10.0, -0.0043),
]


def _interp(x, pts):
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


def _f(x):
    # Central region: interpolate the observed curve directly.
    if -8.0 <= x <= 10.0:
        return _interp(x, _CENTRAL)

    if x > 10.0:
        if x <= 25:
            pts = [(10, -0.0043), (12, -0.0061), (15, -0.0043),
                   (20, -0.0013), (25, -0.0004)]
            return _interp(x, pts)
        elif x <= 60:
            return -0.0004
        else:
            pts = [(60, -0.0004), (85, -0.0002), (112, -0.0001),
                   (128, -0.0001)]
            return _interp(x, pts)
    else:
        # x < -8: monotone far field, smoothly continuing from -0.0002 at -8.
        ax = -x
        pts = [(8, -0.0002), (10, -0.0004), (12, -0.0005), (15, -0.0008),
               (20, -0.0012), (25, -0.0017), (30, -0.0021), (35, -0.0026),
               (40, -0.0030), (45, -0.0032), (50, -0.0032), (60, -0.0032),
               (70, -0.0034), (80, -0.0035), (90, -0.0037), (104, -0.0040),
               (120, -0.0043), (128, -0.0044)]
        return _interp(ax, pts)

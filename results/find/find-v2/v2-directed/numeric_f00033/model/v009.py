import math

def predict(probe):
    # Observations / beliefs:
    # - The function is smooth and mostly small-amplitude, with a positive bump near x ~ 0
    #   and a negative dip near x ~ 12. [E1, E2, E3, E6, E12]
    # - Peak of positive bump is ~0.3868 at x=0, falling to ~0.255 at x=1 and ~0.12 at x=2. [E1,E2,E7,E8]
    # - There is a kink / change of slope near x ~ -2.5..-2.2 (values jump from ~0.022 at -2.5
    #   to ~0.0575 at -2, steeper than smooth continuation). [E2,E11,E13]
    # - Another kink near x ~ 4.0..4.4: the descent from the positive bump changes slope
    #   (0.0099 at 4.0, 0.0071 at 4.2, 0.0043 at 4.4, then tiny values). [E15,E3]
    # - Negative dip centered around x ~ 11.75..12 with min ~ -0.0062. [E6,E12]
    # - For large |x|, values approach small negative constants: ~ -0.0044 at x=-128,
    #   ~0 at x=+128. [E1,E5]
    # - The function appears even-ish in the bump but not exactly; treat as general smooth curve.
    # - No nulls observed; defined on all real inputs tested.
    #
    # Model: piecewise smooth interpolation using cubic Hermite / linear blend over
    # anchor points derived from the evidence, with special handling of the kinks.

    xs = probe.get("x", [])
    ys = []
    for xv in xs:
        try:
            x = float(xv)
        except Exception:
            ys.append(None)
            continue
        ys.append(_f(x))
    return {"y": ys}


# Anchor table: (x, y). Built from evidence, smoothed.
# We'll interpolate with a monotone-ish cubic (Catmull-Rom style) but clamp at ends.
_ANCHORS = [
    (-128.0, -0.0044),
    (-116.0, -0.0042),
    (-104.0, -0.0040),
    (-88.0,  -0.0037),
    (-72.0,  -0.0034),
    (-56.0,  -0.0032),
    (-40.0,  -0.0030),
    (-32.0,  -0.0023),
    (-24.0,  -0.0016),
    (-16.0,  -0.0009),
    (-12.0,  -0.0005),
    (-10.0,  -0.0004),
    (-8.0,   -0.0002),
    (-6.0,    0.0000),
    (-5.5,    0.0014),
    (-5.0,    0.0027),
    (-4.5,    0.0040),
    (-4.0,    0.0053),
    (-3.5,    0.0066),
    (-3.0,    0.0080),
    (-2.75,   0.0111),
    (-2.5,    0.0221),
    (-2.25,   0.0370),
    (-2.0,    0.0575),
    (-1.75,   0.0780),
    (-1.5,    0.1052),
    (-1.25,   0.1467),
    (-1.0,    0.1972),
    (-0.75,   0.2512),
    (-0.5,    0.3052),
    (-0.25,   0.3592),
    (-0.1,    0.3855),
    (0.0,     0.3868),
    (0.1,     0.3760),
    (0.25,    0.3563),
    (0.5,     0.3225),
    (0.75,    0.2888),
    (1.0,     0.2550),
    (1.25,    0.2213),
    (1.5,     0.1875),
    (1.75,    0.1537),
    (2.0,     0.1200),
    (2.25,    0.0890),
    (2.5,     0.0642),
    (2.75,    0.0465),
    (3.0,     0.0327),
    (3.25,    0.0248),
    (3.5,     0.0185),
    (3.75,    0.0138),
    (4.0,     0.0099),
    (4.2,     0.0071),
    (4.4,     0.0043),
    (4.6,     0.0016),
    (4.8,     0.0014),
    (5.0,     0.0012),
    (5.5,     0.0006),
    (6.0,     0.0001),
    (6.5,    -0.0005),
    (7.0,    -0.0010),
    (7.5,    -0.0015),
    (8.0,    -0.0021),
    (8.5,    -0.0026),
    (9.0,    -0.0032),
    (9.5,    -0.0037),
    (10.0,   -0.0043),
    (10.5,   -0.0048),
    (11.0,   -0.0054),
    (11.25,  -0.0056),
    (11.5,   -0.0059),
    (11.75,  -0.0062),
    (12.0,   -0.0061),
    (12.5,   -0.0058),
    (13.0,   -0.0055),
    (13.5,   -0.0052),
    (14.0,   -0.0049),
    (14.5,   -0.0046),
    (15.0,   -0.0043),
    (15.5,   -0.0040),
    (16.0,   -0.0037),
    (17.0,   -0.0031),
    (18.0,   -0.0025),
    (19.0,   -0.0019),
    (20.0,   -0.0013),
    (21.0,   -0.0007),
    (22.0,   -0.0004),
    (23.0,   -0.0004),
    (24.0,   -0.0004),
    (26.0,   -0.0004),
    (28.0,   -0.0004),
    (30.0,   -0.0004),
    (36.0,   -0.0003),
    (40.0,   -0.0004),
    (44.0,   -0.0004),
    (52.0,   -0.0004),
    (56.0,   -0.0004),
    (60.0,   -0.0004),
    (64.0,   -0.0004),
    (72.0,   -0.0003),
    (84.0,   -0.0002),
    (96.0,   -0.0002),
    (100.0,  -0.0002),
    (110.0,  -0.0001),
    (120.0,  -0.0001),
    (128.0,   0.0000),
]

_XS = [a[0] for a in _ANCHORS]
_YS = [a[1] for a in _ANCHORS]


def _f(x):
    # Clamp outside range
    if x <= _XS[0]:
        return _YS[0]
    if x >= _XS[-1]:
        return _YS[-1]

    # Find interval
    lo, hi = 0, len(_XS) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if _XS[mid] <= x:
            lo = mid
        else:
            hi = mid

    x0, x1 = _XS[lo], _XS[hi]
    y0, y1 = _YS[lo], _YS[hi]

    # Linear interpolation is robust and matches dense anchors closely.
    t = (x - x0) / (x1 - x0)
    return y0 + t * (y1 - y0)

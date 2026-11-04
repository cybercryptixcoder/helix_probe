import math

def predict(probe):
    # Mechanism inferred from the evidence:
    # - The MLP implements a piecewise function of x.
    # - Dead zone: for roughly -50 < x < 52, output is constant -84.3663 [E1,E2,E4,E5,E7].
    # - Boundaries: left edge between -51 and -50 [E3,E4]; right edge between 51 and 52 [E5].
    # - Left branch (x <= -50): rises steeply as x decreases; nearly linear in x [E1,E3,E4,E6].
    # - Right branch (x >= 52): rises with x; very steep, roughly linear at large x [E2,E5,E6,E8,E10,E11].
    # - The right branch has a small kink/curvature near x~56-64 [E8,E9], but overall smooth.
    # - Values are symmetric-ish? No: left at -128 = 326549.8, right at 128 = 258084.0.
    # - Best model: piecewise linear interpolation with a few anchor points,
    #   plus smooth extrapolation. Use linear fits per region.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        ys.append(_f(float(x)))
    return {"y": ys}

# Anchor points taken as mechanism (piecewise-linear approximation of the MLP)
# Left branch anchors (x, y) from E1/E3/E4/E6
_LEFT = [
    (-128, 326549.8085),
    (-112, 256101.5362),
    (-96, 185653.2639),
    (-80, 115204.9916),
    (-64, 44756.7193),
    (-63, 40353.7023),
    (-62, 35950.6853),
    (-61, 31826.7695),
    (-60, 27779.3796),
    (-59, 23731.9897),
    (-58, 19684.5999),
    (-57, 15637.21),
    (-56, 12306.9177),
    (-54, 7080.4295),
    (-52, 1853.9413),
    (-51, -84.3663),
]
# Dead zone
_DEAD_LO = -51.0
_DEAD_HI = 51.0
_DEAD_VAL = -84.3663

# Right branch anchors from E5/E8/E10/E11
_RIGHT = [
    (51, 12.4118),
    (52, 428.046),
    (53, 843.6803),
    (54, 1259.3145),
    (55, 1674.9487),
    (56, 2090.5829),
    (57, 3230.3677),
    (58, 4433.2432),
    (59, 5636.1187),
    (60, 6838.9942),
    (61, 8041.8696),
    (62, 10136.592),
    (63, 13053.9381),
    (64, 15971.2842),
    (65, 18888.6303),
    (66, 21805.9764),
    (68, 28208.669),
    (70, 35110.0497),
    (72, 42011.4303),
    (74, 49565.7195),
    (76, 57288.6179),
    (78, 65011.5164),
    (80, 72734.4149),
    (84, 88180.2118),
    (88, 103626.0088),
    (92, 119071.8058),
    (96, 134517.6027),
    (100, 149963.3997),
    (104, 165409.1966),
    (108, 180854.9936),
    (112, 196300.7905),
    (116, 211746.5875),
    (120, 227192.3844),
    (128, 258083.9783),
]

def _interp(anchors, x):
    # linear interpolation/extrapolation using nearest two anchors
    if x <= anchors[0][0]:
        (x0, y0), (x1, y1) = anchors[0], anchors[1]
        return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    if x >= anchors[-1][0]:
        (x0, y0), (x1, y1) = anchors[-2], anchors[-1]
        return y1 + (y1 - y0) * (x - x1) / (x1 - x0)
    for i in range(len(anchors) - 1):
        x0, y0 = anchors[i]
        x1, y1 = anchors[i + 1]
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return anchors[-1][1]

def _f(x):
    if _DEAD_LO <= x <= _DEAD_HI:
        return _DEAD_VAL
    if x < _DEAD_LO:
        return _interp(_LEFT, x)
    return _interp(_RIGHT, x)

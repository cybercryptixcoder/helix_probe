import math

def predict(probe):
    # Mechanism inferred from the evidence:
    # - The MLP implements a piecewise function of x.
    # - Dead zone: for roughly -51 < x < 51, output is constant -84.3663 [E1,E2,E4,E5,E7,E12].
    # - Left edge: at x=-51 output is still -84.3663; ramp begins just below -51 [E3,E4].
    # - Right edge: at x=51 output is 12.4118 (already off plateau); plateau ends at x=51 [E5,E12].
    #   So the dead zone is [-51, 51) with f(51)=12.4118, i.e. plateau up to but not including 51.
    # - Left branch (x <= -51): rises steeply as x decreases; nearly linear in x [E1,E3,E4,E6].
    # - Right branch (x >= 51): rises with x; piecewise-linear with slope changes [E5,E8,E9,E10,E11,E12].
    # - Right ramp is piecewise-linear with breakpoints at integers; slope ~415.8 in [51,56],
    #   then ~1140 in [56,62], then ~1658.7 from 62 onward [E8,E9,E10,E11,E12].
    # - Outer right branch (x>=62) is a straight line slope ~1658.67 [E10,E11].

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(_f(float(x)))
        except Exception:
            ys.append(None)
    return {"y": ys}

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

# Dead zone: plateau value for -51 <= x < 51
_DEAD_LO = -51.0
_DEAD_HI = 51.0
_DEAD_VAL = -84.3663

# Right branch anchors from E5/E8/E9/E10/E11/E12
_RIGHT = [
    (51, 12.4118),
    (51.25, 116.3204),
    (51.5, 220.2289),
    (51.75, 324.1375),
    (52, 428.046),
    (52.25, 531.9546),
    (52.5, 635.8631),
    (53, 843.6803),
    (53.5, 1051.4974),
    (54, 1259.3145),
    (54.5, 1467.1316),
    (55, 1674.9487),
    (55.25, 1778.8573),
    (55.5, 1882.7658),
    (55.75, 1986.6744),
    (56, 2090.5829),
    (56.25, 2328.2111),
    (56.5, 2628.93),
    (56.75, 2929.6488),
    (57, 3230.3677),
    (57.25, 3531.0866),
    (57.5, 3831.8054),
    (57.75, 4132.5243),
    (58, 4433.2432),
    (58.5, 5034.6809),
    (59, 5636.1187),
    (60.5, 7440.4319),
    (61.5, 8680.1872),
    (62, 10136.592),
    (62.25, 10865.9285),
    (62.5, 11595.265),
    (62.75, 12324.6015),
    (63, 13053.9381),
    (63.25, 13783.2746),
    (63.5, 14512.6111),
    (63.75, 15241.9477),
    (64, 15971.2842),
    (64.25, 16700.6207),
    (64.5, 17429.9572),
    (64.75, 18159.2938),
    (65, 18888.6303),
    (66, 21805.9764),
    (67, 24757.9787),
    (68, 28208.669),
    (69, 31659.3593),
    (70, 35110.0497),
    (71, 38560.74),
    (72, 42011.4303),
    (73, 45704.2702),
    (74, 49565.7195),
    (75, 53427.1687),
    (76, 57288.6179),
    (77, 61150.0672),
    (78, 65011.5164),
    (79, 68872.9657),
    (80, 72734.4149),
    (81, 76595.8641),
    (83, 84318.7626),
    (84, 88180.2118),
    (85, 92041.6611),
    (87, 99764.5596),
    (88, 103626.0088),
    (89, 107487.458),
    (91, 115210.3565),
    (92, 119071.8058),
    (93, 122933.255),
    (95, 130656.1535),
    (96, 134517.6027),
    (97, 138379.0519),
    (99, 146101.9504),
    (100, 149963.3997),
    (101, 153824.8489),
    (103, 161547.7474),
    (104, 165409.1966),
    (108, 180854.9936),
    (112, 196300.7905),
    (116, 211746.5875),
    (120, 227192.3844),
    (128, 258083.9783),
]

def _interp(anchors, x):
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
    if _DEAD_LO <= x < _DEAD_HI:
        return _DEAD_VAL
    if x < _DEAD_LO:
        return _interp(_LEFT, x)
    return _interp(_RIGHT, x)

import math

def predict(probe):
    # Beliefs:
    # - Output is a constant baseline -84.3663 on a central interval. [E1,E2,E4,E7,E16]
    # - Central flat region: approximately -51 <= x <= 50.7. [E3,E4,E12,E18,E19]
    #   Left edge: flat for x >= -51.0 (E19: -51.0 flat, -51.1 flat, -51.2 = -84.37,
    #     -51.3 = 24.67 -> so flat starts at -51.2). Actually E19: -51.2 -> -84.3663,
    #     -51.3 -> 24.6704. So flat region begins at x = -51.2 (inclusive).
    #   Right edge: E18: 50.7 -> -84.3663, 50.8 -> -70.715. So flat ends at 50.7.
    # - Left branch: linear for x <= -64 with slope -4403.0. [E13,E14]
    #   f(x) = 326549.8085 - 4403.0*(x+128) for x <= -64.
    # - Right branch: linear for x >= 76 with slope 3861.25. [E10,E11,E15,E17]
    #   f(x) = 57288.6179 + 3861.25*(x-76) for x >= 76.
    # - Transitions are smooth curves between the flat region and the linear branches.
    #   Left transition: from x=-64 to x=-51.2. [E3,E13,E19]
    #   Right transition: from x=50.7 to x=76. [E5,E8,E9,E12,E18]
    # - The left transition near the plateau is a sharp linear ramp:
    #   E19: -52 -> 1853.94, -51.9 -> 1592.62, ... slope ~ -2613.24 per unit.
    #   From -52 to -51.2: 1853.94 + (-2613.24)*(x+52). At -51.2: 1853.94-2613.24*0.8
    #   = 1853.94-2090.59 = -236.65? But observed -84.37 at -51.2. Hmm.
    #   Let's check: -51.3 -> 24.6704, -51.2 -> -84.3663. Slope = (-84.37-24.67)/0.1 = -1090.
    #   So the ramp steepens near the plateau. Actually E19 values:
    #   -52.0: 1853.94, -51.9: 1592.62 (diff -261.32), -51.8: 1331.29 (-261.32),
    #   -51.7: 1069.97 (-261.32), -51.6: 808.64 (-261.32), -51.5: 547.32 (-261.32),
    #   -51.4: 285.99 (-261.32), -51.3: 24.67 (-261.32), -51.2: -84.37 (-109.04).
    #   So linear ramp slope -2613.2 from -52 to -51.3, then a sharp drop to plateau.
    #   The MLP has a sharp transition. Model as: linear ramp from -52 to -51.3,
    #   then linear from (-51.3, 24.67) to (-51.2, -84.37), then flat.
    # - Right transition near plateau (E18): 50.7 -> -84.37, 50.8 -> -70.715,
    #   50.85 -> -49.93, 50.9 -> -29.15, 50.92 -> -20.84, 50.94 -> -12.53,
    #   50.96 -> -4.21, 50.98 -> 4.10, 50.99 -> 8.26, 50.995 -> 10.33,
    #   50.999 -> 12.00, 51.0 -> 12.41, 51.001 -> 12.83, 51.005 -> 14.49,
    #   51.01 -> 16.57, 51.02 -> 20.72, 51.05 -> 33.19, 51.1 -> 53.98.
    #   This is a smooth curve. Then continues via E12/E5/E8/E9 to x=76.
    # - Model: piecewise linear interpolation through anchor points, with
    #   linear extrapolation outside the anchor range. Anchors chosen to
    #   capture the observed structure densely near transitions.
    
    anchors = [
        # Left far linear (slope -4403)
        (-128, 326549.8085),
        (-120, 291325.6723),
        (-112, 256101.5362),
        (-104, 220877.4),
        (-96, 185653.2639),
        (-88, 150429.1278),
        (-80, 115204.9916),
        (-72, 79980.8555),
        (-68, 62368.7874),
        (-66, 53562.7534),
        (-65, 49159.7364),
        (-64, 44756.7193),
        # Left transition (E13, E3)
        (-63.5, 42555.2108),
        (-63, 40353.7023),
        (-62.5, 38152.1938),
        (-62, 35950.6853),
        (-61.5, 33888.7274),
        (-61, 31826.7695),
        (-60.5, 29803.0745),
        (-60, 27779.3796),
        (-59, 23731.9897),
        (-58, 19684.5999),
        (-57, 15637.21),
        (-56, 12306.9177),
        (-54, 7080.4295),
        (-52, 1853.9413),
        # Left sharp ramp (E19): slope -2613.2 from -52 to -51.3
        (-51.9, 1592.6169),
        (-51.8, 1331.2925),
        (-51.7, 1069.9681),
        (-51.6, 808.6437),
        (-51.5, 547.3193),
        (-51.4, 285.9948),
        (-51.3, 24.6704),
        (-51.2, -84.3663),
        # Flat region
        (-50, -84.3663),
        (0, -84.3663),
        (50.5, -84.3663),
        (50.6, -84.3663),
        (50.7, -84.3663),
        # Right transition near plateau (E18)
        (50.8, -70.715),
        (50.85, -49.9333),
        (50.9, -29.1516),
        (50.92, -20.8389),
        (50.94, -12.5263),
        (50.96, -4.2136),
        (50.98, 4.0991),
        (50.99, 8.2555),
        (50.995, 10.3336),
        (50.999, 11.9962),
        (51.0, 12.4118),
        (51.001, 12.8274),
        (51.005, 14.49),
        (51.01, 16.5681),
        (51.02, 20.7245),
        (51.05, 33.1935),
        (51.1, 53.9752),
        # Right transition (E12, E5, E8, E9)
        (51.25, 116.3204),
        (51.5, 220.2289),
        (51.75, 324.1375),
        (52.0, 428.046),
        (52.5, 635.8631),
        (53.0, 843.6803),
        (53.5, 1051.4974),
        (54.0, 1259.3145),
        (54.5, 1467.1316),
        (55.0, 1674.9487),
        (55.5, 1882.7658),
        (56.0, 2090.5829),
        (56.5, 2628.93),
        (57.0, 3230.3677),
        (57.5, 3831.8054),
        (58.0, 4433.2432),
        (58.5, 5034.6809),
        (59.0, 5636.1187),
        (60.5, 7440.4319),
        (61.5, 8680.1872),
        (62.0, 10136.592),
        (62.5, 11595.265),
        (63.0, 13053.9381),
        (63.5, 14512.6111),
        (64.0, 15971.2842),
        (64.5, 17429.9572),
        (65.0, 18888.6303),
        (66.0, 21805.9764),
        (68.0, 28208.669),
        (70.0, 35110.0497),
        (72.0, 42011.4303),
        (74.0, 49565.7195),
        (76.0, 57288.6179),
        # Right far linear (slope 3861.25)
        (78.0, 65011.5164),
        (80.0, 72734.4149),
        (84.0, 88180.2118),
        (88.0, 103626.0088),
        (92.0, 119071.8058),
        (96.0, 134517.6027),
        (100.0, 149963.3997),
        (104.0, 165409.1966),
        (108.0, 180854.9936),
        (112.0, 196300.7905),
        (116.0, 211746.5875),
        (120.0, 227192.3844),
        (128.0, 258083.9783),
    ]
    anchors.sort()
    
    def interp(x):
        if x <= anchors[0][0]:
            x0, y0 = anchors[0]
            x1, y1 = anchors[1]
            slope = (y1 - y0) / (x1 - x0)
            return y0 + slope * (x - x0)
        if x >= anchors[-1][0]:
            x0, y0 = anchors[-2]
            x1, y1 = anchors[-1]
            slope = (y1 - y0) / (x1 - x0)
            return y1 + slope * (x - x1)
        lo, hi = 0, len(anchors) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if anchors[mid][0] <= x:
                lo = mid
            else:
                hi = mid
        x0, y0 = anchors[lo]
        x1, y1 = anchors[hi]
        if x1 == x0:
            return y0
        t = (x - x0) / (x1 - x0)
        return y0 + t * (y1 - y0)
    
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(interp(float(x)))
        except Exception:
            ys.append(None)
    return {"y": ys}

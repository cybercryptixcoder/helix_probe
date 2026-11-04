import math

def predict(probe):
    # Beliefs:
    # The function is smooth everywhere; there is no separate "oscillatory region".
    # It looks like a single smooth bump/dip structure superimposed on a gentle
    # global trend. The apparent "oscillation" was just coarse sampling of a
    # smooth curve with a peak near x=-2 and a sharp dip near x=1. [E8,E10]
    #
    # Left outer (x <= -14): linear, slope ~ -0.00029, from (-128,0.0479) to (-14,0.0142) [E2,E4]
    # Right outer (x >= 26): linear, slope ~ +0.00029, from (26,0.0014) to (128,0.0565) [E6]
    #
    # Interior [-14,26]: smooth curve. Key structure:
    #   rises from 0.0142 at x=-14 up to a peak ~0.0784 at x=-2 [E4,E10]
    #   then falls steeply through 0 near x~0.2 to a min ~-0.0951 at x=1 [E8,E10]
    #   then rises smoothly back toward ~0 at x=26 [E8,E4]
    # Between x=-8 and x=-2 the curve is nearly linear (0.031 -> 0.0784), slope ~0.0079/unit [E10]
    # Between x=-2 and x=-1 it's flat-ish (0.0784 -> 0.0776) [E10]
    # Between x=-1 and x=0 it drops steeply (0.0776 -> -0.0008) [E10]
    # Between x=0 and x=1 it drops to the min (0 -> -0.0951) [E10]
    # Then recovers: 1 -> -0.0951, 1.5 -> -0.0782, 2 -> -0.0595, 2.5 -> -0.0507 [E8,E10]
    #   and continues smoothly: 3 -> -0.0466, 4 -> -0.0438, 6 -> -0.0371, 8 -> -0.03,
    #   10 -> -0.0249, 14 -> -0.0167, 18 -> -0.0084, 22 -> -0.0008, 26 -> 0.0014 [E4,E8]
    # The tail from x=2.5 to 26 is nearly linear with slope ~+0.0013/unit [E8,E4]

    # Dense anchors capturing the smooth curve, especially near the peak and dip [E4,E8,E10]
    anchors = [
        (-14.0, 0.0142),
        (-12.0, 0.0187),
        (-10.0, 0.0249),
        (-8.0, 0.0310),
        (-7.0, 0.0389),
        (-6.0, 0.0471),
        (-5.0, 0.0550),
        (-4.0, 0.0628),
        (-3.0, 0.0706),
        (-2.5, 0.0745),
        (-2.0, 0.0784),
        (-1.5, 0.0780),
        (-1.0, 0.0776),
        (-0.5, 0.0490),
        (0.0, -0.0008),
        (0.5, -0.0484),
        (1.0, -0.0951),
        (1.5, -0.0782),
        (2.0, -0.0595),
        (2.5, -0.0507),
        (3.0, -0.0466),
        (4.0, -0.0438),
        (6.0, -0.0371),
        (8.0, -0.0300),
        (10.0, -0.0249),
        (14.0, -0.0167),
        (18.0, -0.0084),
        (22.0, -0.0008),
        (26.0, 0.0014),
    ]

    out = []
    for x in probe["x"]:
        try:
            if x <= -14.0:
                y = 0.0142 + (x + 14.0) * (0.0479 - 0.0142) / (-128.0 + 14.0)
            elif x >= 26.0:
                y = 0.0014 + (x - 26.0) * (0.0565 - 0.0014) / (128.0 - 26.0)
            else:
                y = None
                for i in range(len(anchors) - 1):
                    x0, y0 = anchors[i]
                    x1, y1 = anchors[i + 1]
                    if x0 <= x <= x1:
                        t = (x - x0) / (x1 - x0)
                        y = y0 + t * (y1 - y0)
                        break
                if y is None:
                    y = 0.0
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

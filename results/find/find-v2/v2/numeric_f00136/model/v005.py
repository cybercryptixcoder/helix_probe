import math

def predict(probe):
    # Beliefs:
    # Outside [-14,26]: smooth linear trend, slope ~+0.00029 on right, ~-0.00029 on left [E2,E4,E6]
    # Inside [-14,26]: oscillatory region with a sharp negative dip near x~1 and peak near x~-2 [E4,E8]
    # E8 shows: peak ~0.078 at x=-1.5, crosses zero ~x=0.3, min ~-0.095 at x=1, then rises
    #   smoothly to ~-0.05 at x=2.5, then a slow linear rise from -0.05 toward -0.024 at x=10.5
    # So the "oscillation" is really one sharp dip near x~1, then a smooth recovery [E8]
    # The earlier anchors (x=6 -> -0.037, x=10 -> -0.025) match E8's smooth tail [E4,E8]
    # Left side of middle: x=-14 -> 0.0142, x=-10 -> 0.0249, x=-6 -> 0.0471, x=-2 -> 0.0784 [E4]
    #   rising smoothly; E8 x=-1.5 -> 0.078, x=-0.5 -> 0.049 (falling after peak near -2) [E8]
    # Right outer: x=26 -> 0.0014, x=128 -> 0.0565, linear slope ~0.00029 [E6]
    # Left outer: x=-128 -> 0.0479, x=-14 -> 0.0142, linear slope ~-0.00029 [E2,E4]

    # Anchor points for the middle region, dense near the dip [E4,E8]
    # (x, y) sorted
    anchors = [
        (-14.0, 0.0142),
        (-12.0, 0.0187),
        (-10.0, 0.0249),
        (-6.0, 0.0471),
        (-2.0, 0.0784),
        (-1.5, 0.0780),
        (-0.5, 0.0490),
        (0.5, -0.0484),
        (1.0, -0.0951),
        (1.5, -0.0782),
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
                # linear from (-128, 0.0479) to (-14, 0.0142)
                y = 0.0142 + (x + 14.0) * (0.0479 - 0.0142) / (-128.0 + 14.0)
            elif x >= 26.0:
                # linear from (26, 0.0014) to (128, 0.0565)
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

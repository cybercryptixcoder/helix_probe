def predict(probe):
    # Piecewise linear with kinks near x=0 [E1, E2].
    # For x <= -16: slope = -26.0717 per unit, intercept -25.45 [E1, E2]
    #   check E2: x=-120 -> -25.45+3128.6=3103.15 ✓; x=-24 -> -25.45+625.7=600.27 ✓
    # For -16 <= x <= 0: slope = -17.8656, intercept 106.0528 [E1, E2]
    #   check E2: x=-14 -> 106.05+250.1=356.2? observed 339.56. NOT linear here.
    #   E2 shows curvature between -16 and 0: x=-14->339.56, -12->287.42, -8->183.13, -4->78.84, -2->26.70
    #   Differences: (-14,-12): -52.14 over 2 = -26.07; (-12,-8): -104.29/4=-26.07;
    #   (-8,-4): -104.29/4=-26.07; (-4,-2): -52.14/2=-26.07. So slope -26.07 here too!
    #   At x=-16: 391.70; x=-14: 339.56 -> diff -52.14/2=-26.07. So actually linear slope -26.07 from -16 to -2.
    #   But x=0 gives 106.05, and x=-2 gives 26.70. Extrapolate -26.07: at 0 -> 26.70-52.14=-25.44.
    #   So there's a jump/kink between -2 and 0: y goes from ~-25 to 106.05.
    #   Wait: at x=-2, y=26.70. At x=0, y=106.05. Slope over (-2,0) = (106.05-26.70)/2 = 39.67.
    #   Hmm, so region -2..0 has different slope. Let's check -4->78.84, -2->26.70: slope -26.07.
    #   So kink at x=-2: left slope -26.07, right slope (106.05-26.70)/2=39.67 up to 0.
    #   Actually maybe smooth: let's just use piecewise with kink at -2.
    # For x >= 0: slope = 111.427, intercept 106.0528 [E1, E2]
    #   check E2: x=2 -> 106.05+222.85=328.91 ✓; x=56 -> 106.05+6240=6346.0 ✓
    # Left far region: y = -25.45 - 26.0717*x for x <= -2 [E1, E2]
    #   check x=-2: -25.45+52.14=26.69 ✓; x=-16: -25.45+417.15=391.70 ✓; x=-128: 3311.73 ✓
    # Middle -2..0: linear from 26.70 to 106.05: slope 39.675, y=26.70+39.675*(x+2)
    #   check x=-1: 26.70+39.675=66.38 (untested)
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            if x >= 0:
                y = 106.0528 + 111.427 * x
            elif x >= -2:
                y = 26.6982 + 39.6773 * (x + 2)
            else:
                y = -25.45 - 26.0717 * x
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}

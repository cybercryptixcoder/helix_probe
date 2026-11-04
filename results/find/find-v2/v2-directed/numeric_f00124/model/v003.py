def predict(probe):
    # Far-left branch: y = -25.45 - 26.0717*x, valid for x <= -2 [E1, E2]
    #   checks: x=-128 -> 3311.73, x=-24 -> 600.28, x=-3 -> 52.77 ✓
    # At x=-2.5 y=39.73, x=-2 y=26.70: slope -26.07 continues to x=-2 [E2, E3]
    # At x=-1.5 y=13.66, x=-1 y=6.85: slope ~ -13.6 here, NOT -26.07 [E3]
    #   So kink at x=-2: left slope -26.07, right slope ~ -13.6 [E3]
    #   check: -2 -> 26.70; -1.5 -> 26.70-13.6*0.5=19.9? observed 13.66. Not quite.
    #   Try slope from -2 to -1.5: (13.66-26.70)/0.5 = -26.07. Still -26.07!
    #   From -1.5 to -1: (6.85-13.66)/0.5 = -13.62. Kink at x=-1.5.
    #   From -1 to -0.5: (50.34-6.85)/0.5 = +86.98. Kink at x=-1.
    #   From -0.5 to -0.25: (78.20-50.34)/0.25 = +111.4. Slope 111.4 (= right branch slope!)
    #   From -0.25 to -0.1: (94.91-78.20)/0.15 = +111.4. Same slope 111.4.
    #   So for x >= -0.5: slope 111.427, and at x=-0.5: 50.34 -> intercept 50.34+0.5*111.427=106.05 ✓
    #   So the right branch y=106.05+111.427*x extends down to x=-0.5? check x=-0.5: 106.05-55.7=50.35 ✓
    #   And x=-1: 106.05-111.4=-5.4, but observed 6.85. So kink at x=-0.5.
    # Region -1.5 to -1: slope -13.62, at x=-1: 6.85 -> intercept 6.85-13.62=... y=6.85+(-13.62)*(x+1)
    #   check x=-1.5: 6.85+(-13.62)*(-0.5)=13.66 ✓
    # Region -1 to -0.5: slope +86.98, at x=-1: 6.85 -> y=6.85+86.98*(x+1)
    #   check x=-0.5: 6.85+43.49=50.34 ✓
    # Region -2 to -1.5: slope -26.07, at x=-2: 26.70 -> y=26.70-26.07*(x+2)
    #   check x=-1.5: 26.70-13.04=13.66 ✓
    # So piecewise: x<=-2: -25.45-26.0717x; -2..-1.5: 26.70-26.07(x+2);
    #   -1.5..-1: 6.85-13.62(x+1); -1..-0.5: 6.85+86.98(x+1);
    #   x>=-0.5: 106.0528+111.427x
    # Note -2..-1.5 has same slope as far-left, so merge: x<=-1.5: -25.45-26.0717x
    #   check x=-1.5: -25.45+39.11=13.66 ✓
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            if x >= -0.5:
                y = 106.0528 + 111.427 * x
            elif x >= -1:
                y = 6.8494 + 86.98 * (x + 1)
            elif x >= -1.5:
                y = 6.8494 - 13.62 * (x + 1)
            else:
                y = -25.45 - 26.0717 * x
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}

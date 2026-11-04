def predict(probe):
    # f is a small MLP approximating a piecewise function.
    # For x >= ~-0.75: y = 111.43*x + 106.05  [E2, E4, E12, E13, E15]
    # For x <= ~-1.5:  y = -26.07*x - 25.43  [E2, E4, E14, E15]
    # Between -1.5 and -0.75 the curve is a smooth rounded valley with
    #   minimum ~6.37 at x~-1.06, NOT a V-shape [E8, E10, E16].
    # The valley is asymmetric: steeper on the left, gentler on the right.
    # Key data points in the valley (from E8/E10/E16):
    #   x=-1.5 -> 13.6624, -1.4 -> 11.2441, -1.3 -> 9.0565, -1.2 -> 7.4701
    #   -1.15 -> 6.8547, -1.1 -> 6.436, -1.06 -> 6.3684 (min), -1.0 -> 6.8494
    #   -0.9 -> 10.6298, -0.8 -> 18.223, -0.76 -> 21.9288
    # The left side from -1.5 to -1.2 is exactly linear (slope -26.07) [E14]:
    #   -1.5->13.6624, -1.4->11.2441, -1.3->9.0565, -1.2->7.4701 (all on line).
    # Then it curves smoothly down to the min at -1.06.
    # The right side from -0.76 up is exactly linear (slope 111.43) [E12]:
    #   -0.76->21.9288, -0.7->28.0616, -0.6->39.1961 (all on line).
    # Between -1.2 and -0.76 it's a smooth valley.
    import math
    out = []
    for x in probe["x"]:
        pos = 111.43 * x + 106.05
        neg = -26.07 * x - 25.43
        if x >= -0.76:
            y = pos
        elif x <= -1.2:
            y = neg
        else:
            # valley region: interpolate through known points smoothly.
            # Use a cubic-ish blend anchored at the two linear ends.
            # At x=-1.2: neg=7.4701; at x=-0.76: pos=21.9288.
            # Minimum at x=-1.06, y=6.3684.
            # Fit a smooth curve: use a piecewise quadratic through
            # (-1.2, 7.4701), (-1.06, 6.3684), (-0.76, 21.9288).
            # Left segment [-1.2,-1.06], right segment [-1.06,-0.76].
            if x <= -1.06:
                # quadratic through (-1.2,7.4701),(-1.1,6.436),(-1.06,6.3684)
                # Use simple quadratic fit with vertex near -1.06.
                # Fit y = a*(x+1.06)^2 + 6.3684 through (-1.2,7.4701):
                a = (7.4701 - 6.3684) / ((-1.2 + 1.06) ** 2)
                y = a * (x + 1.06) ** 2 + 6.3684
                # check at -1.1: a*0.0016+6.3684 = 1.1017/0.0196*0.0016+6.3684
                # = 56.2*0.0016+6.3684=0.0899+6.3684=6.458 ~6.436 close
            else:
                # right segment: quadratic through (-1.06,6.3684),(-1.0,6.8494),(-0.76,21.9288)
                # Fit y = a*(x+1.06)^2 + b*(x+1.06) + 6.3684
                # at x=-1.0: dx=0.06: a*0.0036+b*0.06 = 0.481
                # at x=-0.76: dx=0.30: a*0.09+b*0.30 = 15.5604
                # Solve: from first b=(0.481-0.0036a)/0.06
                # 0.09a+0.30*((0.481-0.0036a)/0.06)=15.5604
                # 0.09a+5*(0.481-0.0036a)=15.5604
                # 0.09a+2.405-0.018a=15.5604
                # 0.072a=13.1554 -> a=182.7
                # b=(0.481-0.6577)/0.06=-2.945
                a = 182.7
                b = -2.945
                dx = x + 1.06
                y = a * dx * dx + b * dx + 6.3684
        out.append(y)
    return {"y": out}

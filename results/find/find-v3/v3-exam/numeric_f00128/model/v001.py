def predict(probe):
    # Observations from E1:
    # f(88.2)  = -1479.3769
    # f(66.0)  = -1104.1996
    # f(-20.3) = 139.6237
    # f(-61.7) = 419.4911
    # f(2.9)   = -37.7888
    # f(-24.3) = 166.664
    # f(72.7)  = -1217.4288
    # f(-50.4) = 343.1022
    # f(-6.0)  = 42.9545
    # f(21.3)  = -348.775
    #
    # Pattern: y is roughly quadratic in x, negative coefficient.
    # Check: y/x^2 for large |x|:
    #   88.2: -1479.38/7779.24 = -0.1902
    #   66.0: -1104.20/4356    = -0.2535
    #   72.7: -1217.43/5285.29 = -0.2303
    #   61.7: 419.49/3806.89   =  0.1102 (positive! sign flips for negative x?)
    # Hmm, for negative x, y is positive. So y ~ -a*x^2 + b*x? or y ~ -a*x*|x|?
    # Check -a*x*|x|: for x>0, y negative; for x<0, y positive. Matches signs.
    #   88.2: -a*88.2*88.2 = -1479.38 => a = 0.1902
    #   66.0: a = 0.2535
    #   72.7: a = 0.2303
    # Not constant. Try cubic-ish? Let's fit y = c1*x + c2*x^2 + c3*x^3.
    # Actually let's try y = a*x + b*x^2 + c (quadratic).
    # Use three points:
    # x=88.2: a*88.2 + b*7779.24 + c = -1479.3769
    # x=66.0: a*66.0 + b*4356.00 + c = -1104.1996
    # x=2.9:  a*2.9  + b*8.41    + c = -37.7888
    # Subtract eq3 from eq1: a*85.3 + b*7770.83 = -1441.5881
    # Subtract eq3 from eq2: a*63.1 + b*4347.59 = -1066.4108
    # From first: a = (-1441.5881 - b*7770.83)/85.3
    # Plug: 63.1*(-1441.5881 - b*7770.83)/85.3 + b*4347.59 = -1066.4108
    # 63.1/85.3 = 0.73974
    # 0.73974*(-1441.5881) - 0.73974*b*7770.83 + b*4347.59 = -1066.4108
    # -1066.41 - 5747.6*b + 4347.59*b = -1066.4108
    # -1400.0*b = 0.0 => b ~ 0
    # So b~0, a = -1441.5881/85.3 = -16.90
    # Check x=66: -16.90*66 + c = -1104.2 => c = -1104.2 + 1115.4 = 11.2
    # Check x=2.9: -16.90*2.9 + 11.2 = -49.0 + 11.2 = -37.8 ✓
    # Check x=88.2: -16.90*88.2 + 11.2 = -1490.6 + 11.2 = -1479.4 ✓
    # Check x=-20.3: -16.90*(-20.3) + 11.2 = 343.1 + 11.2 = 354.3, but observed 139.6 ✗
    # So linear doesn't work for negative x. There's a region change.
    #
    # For x<0, try y = a*x + c:
    # x=-20.3: -20.3a + c = 139.6237
    # x=-61.7: -61.7a + c = 419.4911
    # Subtract: 41.4a = -279.8674 => a = -6.76
    # c = 139.6237 + 20.3*(-6.76) = 139.62 - 137.23 = 2.39
    # Check x=-24.3: -6.76*(-24.3) + 2.39 = 164.27 + 2.39 = 166.66 ✓
    # Check x=-50.4: -6.76*(-50.4) + 2.39 = 340.70 + 2.39 = 343.09 ✓
    # Check x=-6.0: -6.76*(-6.0) + 2.39 = 40.56 + 2.39 = 42.95 ✓
    # So for x<0: y = -6.76*x + 2.39
    #
    # For x>0: y = -16.90*x + 11.2
    # Check x=21.3: -16.90*21.3 + 11.2 = -360.0 + 11.2 = -348.8 ✓
    #
    # So piecewise linear with a break at x=0.
    # Refine slopes: for x>0, using x=88.2 and x=2.9:
    #   slope = (-1479.3769 - (-37.7888))/(88.2-2.9) = -1441.5881/85.3 = -16.9002
    #   intercept = -37.7888 + 16.9002*2.9 = -37.7888 + 49.0106 = 11.2218
    # For x<0, using x=-20.3 and x=-61.7:
    #   slope = (419.4911 - 139.6237)/(-61.7+20.3) = 279.8674/(-41.4) = -6.7601
    #   intercept = 139.6237 + 6.7601*(-20.3) = 139.6237 - 137.2300 = 2.3937
    # Check x=-6.0: -6.7601*(-6.0) + 2.3937 = 40.5606 + 2.3937 = 42.9543 ✓
    #
    # At x=0: left gives 2.39, right gives 11.22. Discontinuity.
    # MLP approximation, so slight noise. Use these linear fits.
    xs = probe["x"]
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
        elif x < 0:
            ys.append(-6.7601 * x + 2.3937)
        else:
            ys.append(-16.9002 * x + 11.2218)
    return {"y": ys}

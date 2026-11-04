def predict(probe):
    # Model hypothesis from E1:
    # y looks like a cubic-ish / polynomial-ish function of x.
    # Try fitting y = a*x^3 + b*x^2 + c*x + d using E1 data.
    # Check: for x=88.2, y=-1973.3; x=66.0, y=-1473.8; x=-20.3, y=232.267; ...
    # Let's test a simple cubic fit mentally is hard; instead use a piecewise guess.
    #
    # Observations suggest roughly y ~ -0.0029 * x^3? Let's check:
    # 88.2^3 = 686128; -1973.3/686128 ≈ -0.002876
    # 66^3 = 287496; -1473.8/287496 ≈ -0.005126 -> not constant, so not pure cubic.
    #
    # Try quadratic: 88.2^2=7779.24; -1973.3/7779.24 ≈ -0.2537
    # 66^2=4356; -1473.8/4356 ≈ -0.3383 -> not constant either.
    #
    # Try linear: -1973.3/88.2 ≈ -22.37; -1473.8/66 ≈ -22.33; close!
    # -20.3: 232.267/-20.3 ≈ -11.44 -> not linear.
    # Hmm, sign flips: x negative gives positive y for -20.3, but -24.3 gives +275.8, -50.4 gives +560, -61.7 gives +683.
    # For x=-6.0: y=76.54 -> 76.54/-6 = -12.76
    # For x=2.9: y=-54.05 -> -54.05/2.9 = -18.64
    # For x=21.3: y=-468.05 -> -468.05/21.3 = -21.97
    #
    # Looks like y ≈ -22.4*x for large |x|, but smaller slope near 0?
    # Check x=-6: -22.4*-6 = 134.4 vs 76.54. Not matching.
    # Maybe y = -22.4*x + something? x=-6: 134.4 + c = 76.54 -> c=-57.86
    # x=2.9: -22.4*2.9 = -64.96 + c = -54.05 -> c=10.91. Not constant.
    #
    # Try y = a*x + b*x^2? 
    # Use x=88.2: 88.2a + 7779.24b = -1973.3
    # x=66: 66a + 4356b = -1473.8
    # From second: a = (-1473.8 - 4356b)/66 = -22.3303 - 66b
    # Sub: 88.2*(-22.3303-66b) + 7779.24b = -1973.3
    # -1969.53 - 5821.2b + 7779.24b = -1973.3
    # 1958.04b = -3.77 -> b = -0.001925
    # a = -22.3303 - 66*(-0.001925) = -22.3303 + 0.12705 = -22.2033
    # Check x=-20.3: -22.2033*(-20.3) + (-0.001925)*(412.09) = 450.73 - 0.793 = 449.94 vs 232.267. No.
    #
    # Maybe piecewise: for x >= some threshold, slope ~ -22.4; for x < threshold, different.
    # x=-20.3: 232.267; x=-24.3: 275.827. Slope between: (275.827-232.267)/(-24.3+20.3) = 43.56/-4 = -10.89
    # x=-50.4: 560.056; x=-61.7: 683.113. Slope: (683.113-560.056)/(-61.7+50.4)=123.057/-11.3=-10.89
    # x=-24.3 to -50.4: (560.056-275.827)/(-50.4+24.3)=284.229/-26.1=-10.89
    # So for x <= -20.3, slope is -10.89! And y = -10.89*x + c?
    # x=-20.3: -10.89*-20.3 = 221.07 + c = 232.267 -> c=11.2
    # x=-61.7: -10.89*-61.7 = 671.91 + 11.2 = 683.11 ✓
    # So for x <= -20: y ≈ -10.89*x + 11.2
    #
    # For x >= 66: slope between 66 and 88.2: (-1973.3+1473.8)/(88.2-66) = -499.5/22.2 = -22.5
    # y = -22.5*x + c: 66*-22.5 = -1485 + c = -1473.8 -> c=11.2
    # 88.2*-22.5 = -1984.5 + 11.2 = -1973.3 ✓
    # So for x >= 66: y = -22.5*x + 11.2
    #
    # Middle region: x=2.9: -54.05; x=21.3: -468.05. Slope: (-468.05+54.05)/(21.3-2.9) = -414/18.4 = -22.5
    # y = -22.5*x + c: 2.9*-22.5 = -65.25 + c = -54.05 -> c=11.2 ✓
    # 21.3*-22.5 = -479.25 + 11.2 = -468.05 ✓
    # x=-6: -22.5*-6 = 135 + 11.2 = 146.2 vs 76.54. Doesn't match.
    #
    # Hmm. x=-6 gives 76.54. -10.89*-6 = 65.34 + 11.2 = 76.54 ✓!
    # So x=-6 is in the "low slope" region.
    #
    # So threshold between -6 and 2.9? Or between -20.3 and -6?
    # x=-20.3: -10.89*-20.3+11.2 = 232.27 ✓ (low slope region)
    # x=-24.3: -10.89*-24.3+11.2 = 275.83 ✓
    # x=2.9: high slope region
    # So threshold is between -6 and 2.9.
    #
    # Let's guess threshold at 0: for x < 0, slope -10.89; for x >= 0, slope -22.5.
    # Check x=-6: -10.89*-6+11.2 = 76.54 ✓
    # x=-20.3: ✓, x=-24.3: ✓, x=-50.4: -10.89*-50.4+11.2 = 548.86+11.2=560.06 ✓, x=-61.7: ✓
    # x=2.9: -22.5*2.9+11.2 = -65.25+11.2 = -54.05 ✓
    # x=21.3: ✓, x=66: ✓, x=88.2: ✓
    #
    # So: y = -10.89*x + 11.2 for x < 0; y = -22.5*x + 11.2 for x >= 0.
    # Let's refine constants: slope1 = -10.89, slope2 = -22.5, intercept 11.2.
    # From x=-61.7: (683.113-11.2)/-61.7 = 671.913/-61.7 = -10.8900
    # From x=88.2: (-1973.3-11.2)/88.2 = -1984.5/88.2 = -22.5000
    # From x=66: (-1473.8-11.2)/66 = -1485/66 = -22.5
    # From x=-20.3: (232.267-11.2)/-20.3 = 221.067/-20.3 = -10.89
    # Intercept: from x=2.9: -54.05 - (-22.5*2.9) = -54.05+65.25 = 11.2
    # from x=-6: 76.54 - (-10.89*-6) = 76.54-65.34 = 11.2
    # Great, consistent.
    #
    # So model: y = 11.2 + (-10.89 if x<0 else -22.5)*x
    # Threshold at 0 (between -6 and 2.9, likely exactly 0).
    out = []
    for x in probe["x"]:
        slope = -10.89 if x < 0 else -22.5
        out.append(11.2 + slope * x)
    return {"y": out}

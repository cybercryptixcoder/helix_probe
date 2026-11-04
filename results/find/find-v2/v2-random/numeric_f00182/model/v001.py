def predict(probe):
    # Model hypothesis from E1: y looks like a cubic-like function of x.
    # Check: x=88.2 -> -1973.3; x=66 -> -1473.8; x=2.9 -> -54.05; x=-6 -> 76.54
    # Try y = a*x^3 + b*x? Let's test ratios.
    # 88.2^3 = 686128.968; 66^3=287496; 2.9^3=24.389; (-6)^3=-216
    # If y = k*x^3: k from 88.2: -1973.3/686128.968 = -0.002876
    # from 66: -1473.8/287496 = -0.005126 -- not constant.
    # Try y = a*x^3 + b*x.
    # Use x=88.2: a*686128.968 + b*88.2 = -1973.3
    # x=66: a*287496 + b*66 = -1473.8
    # Solve: from second, b = (-1473.8 - 287496a)/66
    # plug: 686128.968a + 88.2*(-1473.8-287496a)/66 = -1973.3
    # 88.2/66 = 1.33636...
    # 686128.968a - 1.33636*287496a - 1.33636*1473.8 = -1973.3
    # 686128.968 - 384, 1.33636*287496 = 384, let's compute: 287496*1.33636=384,  actually 287496*88.2/66 = 287496*1.3363636 = 384,  = 384,  let me: 287496*88.2 = 25,357,147.2; /66 = 384,199.2
    # 686128.968 - 384199.2 = 301929.768
    # 1.33636*1473.8 = 1969.6
    # 301929.768a - 1969.6 = -1973.3 => 301929.768a = -3.7 => a ≈ -1.225e-5
    # b = (-1473.8 - 287496*(-1.225e-5))/66 = (-1473.8 + 3.522)/66 = -1470.28/66 = -22.277
    # Check x=2.9: a*24.389 + b*2.9 = -0.0002988 - 64.6 = -64.6, but observed -54.05. Off.
    # Try y = a*x^3 + b*x^2 + c*x? Or maybe y = a*x^3 + b*x with different fit.
    # Let's use x=2.9 and x=-6:
    # 2.9: 24.389a + 2.9b = -54.05
    # -6: -216a -6b = 76.54
    # From second: b = (76.54+216a)/(-6) = -12.7567 - 36a
    # plug: 24.389a + 2.9*(-12.7567-36a) = -54.05
    # 24.389a - 36.994 - 104.4a = -54.05
    # -80.011a = -17.056 => a = 0.21317
    # b = -12.7567 - 36*0.21317 = -12.7567 - 7.674 = -20.43
    # Check x=88.2: 0.21317*686128.968 + (-20.43)*88.2 = 146,  146,  huge, not -1973.
    # So not cubic globally. Maybe piecewise.
    # Look at signs: x=88.2 -> -1973 (negative), x=66 -> -1473 (negative), x=72.7 -> -1624 (negative)
    # x=-61.7 -> +683 (positive), x=-50.4 -> +560 (positive), x=-24.3 -> +275 (positive), x=-20.3 -> +232 (positive)
    # x=2.9 -> -54, x=-6 -> +76.5, x=21.3 -> -468
    # Hmm x=-6 gives +76.5 but x=2.9 gives -54. Sign flip near 0.
    # Magnitudes: |x|=88.2 -> 1973; |x|=66->1473; |x|=72.7->1624; |x|=61.7->683; |x|=50.4->560; |x|=24.3->275; |x|=20.3->232; |x|=21.3->468; |x|=6->76.5; |x|=2.9->54
    # For negative x: 61.7->683, 50.4->560, 24.3->275, 20.3->232, 6->76.5
    # ratio y/|x|: 61.7:11.07, 50.4:11.11, 24.3:11.32, 20.3:11.43, 6:12.75 -- roughly 11*x for negatives? 
    # Actually y ≈ 11.1*|x| for negative x? 61.7*11.1=685 yes. 50.4*11.1=559 yes. 24.3*11.1=270 close. 20.3*11.1=225 close. 6*11.1=66.6 vs 76.5 hmm.
    # For positive x: 88.2->1973, 66->1473, 72.7->1624, 21.3->468, 2.9->54
    # ratio: 88.2:22.37, 66:22.33, 72.7:22.34, 21.3:21.97, 2.9:18.6
    # So y ≈ -22.35*x for positive x! 88.2*22.35=1971 yes. 66*22.35=1475 yes. 72.7*22.35=1625 yes. 21.3*22.35=476 close. 2.9*22.35=64.8 vs 54 hmm.
    # For negative x: y ≈ -11.1*x (since x negative, -11.1*x positive). 61.7*-11.1=-685 -> +685 yes.
    # So piecewise linear! Slope -22.35 for x>0, slope -11.1 for x<0.
    # But x=2.9: -22.35*2.9=-64.8 vs -54.05. Off. x=6: -11.1*-6=66.6 vs 76.5. Off.
    # Maybe there's a small region near 0 with different slope, or an offset.
    # Let's fit positive: use 88.2,66: slope = (-1973.3+1473.8)/(88.2-66)= -499.5/22.2 = -22.5. intercept: -1973.3 - (-22.5*88.2)= -1973.3+1984.5=11.2
    # Check 72.7: -22.5*72.7+11.2 = -1635.75+11.2=-1624.55 YES exactly!
    # Check 21.3: -22.5*21.3+11.2 = -479.25+11.2=-468.05 YES!
    # Check 2.9: -22.5*2.9+11.2 = -65.25+11.2=-54.05 YES!
    # So for x>0: y = -22.5*x + 11.2
    # Negative: use -61.7, -50.4: slope=(683.113-560.056)/(-61.7+50.4)=123.057/-11.3=-10.89. intercept: 683.113-(-10.89*-61.7)=683.113-671.9=11.2
    # Check -20.3: -10.89*-20.3+11.2=221.07+11.2=232.27 YES!
    # Check -24.3: -10.89*-24.3+11.2=264.6+11.2=275.8 YES!
    # Check -6: -10.89*-6+11.2=65.34+11.2=76.54 YES!
    # So for x<0: y = -10.89*x + 11.2
    # Both share intercept 11.2! Slopes: -22.5 for x>0, -10.89 for x<0.
    # Let's refine slopes. Positive slope: from 88.2 and 66: -22.5 exactly? -499.5/22.2=-22.5. 
    # Negative: 123.057/-11.3 = -10.8891... maybe -10.89.
    # Let's use -10.89: -10.89*-61.7+11.2=671.913+11.2=683.113 YES exact.
    # So model: y = 11.2 + (-22.5 if x>0 else -10.89)*x
    # At x=0? unknown. Use 11.2.
    import math
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        try:
            x = float(x)
            if x > 0:
                y = 11.2 - 22.5*x
            else:
                y = 11.2 - 10.89*x
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

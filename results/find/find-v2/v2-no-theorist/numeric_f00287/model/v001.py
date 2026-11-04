def predict(probe):
    # Model of f(x):
    # For x <= -10: f(x) = -0.7 * x  [E2: -120->84, -10->7, slope -0.7]
    # For x >= 20: f(x) = -16.8 * x  [E2: 20->-336, 100->-1680, slope -16.8]
    # For -10 < x < 20: transition region, noisy values near -402 [E2: 0->-402.29, 10->-402.40]
    #   E1: x=2.9 -> -402.2267, x=-6.0 -> 4.2 (fits left line: -0.7*-6=4.2)
    #   E1: x=21.3 -> -352.8 (fits right line: -16.8*21.3=-357.8, close-ish)
    #   E1: x=-20.3 -> 14.7 (left line: 14.21, close)
    #   E1: x=-24.3 -> 17.5 (left line: 17.01)
    #   E1: x=-50.4 -> 35.7 (left line: 35.28)
    #   E1: x=-61.7 -> 43.4 (left line: 43.19)
    #   E1: x=66.0 -> -1108.8 (right line: -1108.8 exact!)
    #   E1: x=72.7 -> -1209.6 (right line: -1221.36, close)
    #   E1: x=88.2 -> -1478.4 (right line: -1481.76, close)
    # Left line seems slightly off; try slope from E2 exactly: (84-7)/(-120+10)=77/-110=-0.7
    #   E1 left: -20.3*-0.7=14.21 vs 14.7; -24.3*-0.7=17.01 vs 17.5; -50.4*-0.7=35.28 vs 35.7
    #   Differences ~0.5, ~0.5, ~0.4 -> maybe intercept +0.5? 
    #   Check E2: -120*-0.7+0.5=84.5 vs 84.0; -10*-0.7+0.5=7.5 vs 7.0. So intercept 0 fits E2 better.
    #   E1 differences might be noise or rounding. Use slope -0.7, intercept 0 for left.
    # Right line: E2 gives slope -16.8 exactly (20->-336, 100->-1680).
    #   E1: 66->-1108.8 = -16.8*66 exactly. 72.7->-1209.6 vs -1221.36 (diff 11.76)
    #   88.2->-1478.4 vs -1481.76 (diff 3.36). 21.3->-352.8 vs -357.84 (diff 5.04)
    #   Hmm, E1 right values are less negative than -16.8x. Maybe slope slightly less?
    #   Fit E1 right: (66,-1108.8),(72.7,-1209.6),(88.2,-1478.4),(21.3,-352.8)
    #   slope between 66 and 88.2: (-1478.4+1108.8)/(88.2-66)=-369.6/22.2=-16.65
    #   between 21.3 and 66: (-1108.8+352.8)/(66-21.3)=-756/44.7=-16.91
    #   E2 is cleaner: use -16.8.
    # Transition region -10 < x < 20: values near -402 (E2: 0->-402.2897, 10->-402.4037)
    #   E1: 2.9->-402.2267. So roughly constant -402.3 in this region.
    #   But E1: -6.0->4.2 fits left line, so boundary is between -6 and 0? E2 has -10->7 (left line).
    #   E1: 21.3->-352.8 fits right line, so boundary between 10 and 21.3? E2 has 20->-336 (right line).
    #   So transition roughly (-6, 20) or (-10, 20). Use -10 < x < 20 as transition? 
    #   But -6 gives 4.2 (left). So left boundary is between -6 and 0. Try x < 0 -> left line?
    #   E2: -10->7 fits left. E1: -6->4.2 fits left. So left boundary at 0.
    #   Right boundary: E2 20->-336 fits right. E1 21.3->-352.8 fits right. So right boundary at 20.
    #   Transition: 0 <= x < 20 -> ~-402.3
    #   Check E2: 0->-402.2897, 10->-402.4037. Yes.
    #   But E1: 2.9->-402.2267. Yes.
    # So: x < 0: -0.7x; 0 <= x < 20: -402.3; x >= 20: -16.8x
    # Wait, E2: 20->-336 = -16.8*20. And 0->-402.2897. So boundary at 20 for right.
    # But what about x between 0 and 20? E2 only has 0 and 10. Both ~-402.3.
    # E1: 2.9->-402.2267. Consistent.
    # So transition region is [0, 20).
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if x < 0:
                y = -0.7 * x
            elif x < 20:
                y = -402.3
            else:
                y = -16.8 * x
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

import math

def predict(probe):
    # Observations:
    # E1: 88.2->-1478.4, 66->-1108.8, 72.7->-1209.6, 21.3->-352.8 (positive x, large)
    #     ratios: -16.76, -16.8, -16.64, -16.56  => y ≈ -16.8x for x>~3
    # E1: 2.9->-402.4726 ; E2: 1.2->-402.4498  => near zero positive, y ≈ -402.45 CONSTANT
    #     So for 0<x<~3, y is flat ≈ -402.45 (not cubic!)
    # E1: -20.3->14.7, -24.3->17.5, -61.7->43.4, -50.4->35.7, -6->4.2
    # E2: -55.8->39.2, -63.9->44.8  => y ≈ -0.7x for x<0
    # E2: 104.5->-1747.2, 104.9->-1747.2, 123.6->-2066.4, 79.4->-1327.2, 103->-1730.4, 65.5->-1092, 30.3->-504
    #     ratios: -16.72,-16.66,-16.72,-16.72,-16.8,-16.67,-16.63 => y ≈ -16.72x for x>~3
    # Best fit slope for x>3: use -16.72 (E2 large values) vs -16.8 (E1). Try -16.72.
    #   E1 check: 88.2*-16.72=-1474.7 (obs -1478.4); 66*-16.72=-1103.5 (obs -1108.8); 72.7*-16.72=-1215.5 (obs -1209.6)
    #   E2 check: 104.5*-16.72=-1747.2 exact! 123.6*-16.72=-2066.6 (obs -2066.4); 79.4*-16.72=-1327.6 (obs -1327.2)
    #   -16.72 fits E2 well. E1 slightly off. Maybe slope is exactly -16.72? Or -16.7?
    #   104.5*-16.72=-1747.24 ~ -1747.2. 123.6*-16.72=-2066.59 ~ -2066.4. 79.4*-16.72=-1327.57 ~ -1327.2.
    #   Try -16.7: 104.5*-16.7=-1745.15 (obs -1747.2) worse. -16.72 better.
    #   E1: 88.2*-16.72=-1474.7 vs -1478.4 (diff 3.7). Hmm. 66*-16.72=-1103.5 vs -1108.8 (diff 5.3).
    #   Maybe slope -16.75? 104.5*-16.75=-1750.4 (obs -1747.2). Worse for E2.
    #   Compromise -16.72.
    # Negative slope: E1 -6->4.2 => -0.7; -20.3->14.7 => -0.724; -24.3->17.5=>-0.720; -61.7->43.4=>-0.703
    #   E2: -55.8->39.2 => -0.7025; -63.9->44.8 => -0.7011
    #   Best ~ -0.705. Try -0.705: -6*-0.705=4.23 (obs 4.2); -20.3*-0.705=14.31 (obs 14.7) hmm.
    #   -20.3 needs -0.724. -6 needs -0.7. Varies. Use -0.71 average.
    # Near-zero positive plateau: 2.9->-402.4726, 1.2->-402.4498. Both ≈ -402.45.
    #   Boundary: where does plateau meet linear? -16.72x = -402.45 -> x=24.07. But 21.3->-352.8 = -16.56*21.3, linear!
    #   So 21.3 is linear (-352.8), 2.9 is plateau (-402.45). Boundary between 2.9 and 21.3.
    #   Hmm 21.3*-16.72=-356.2 (obs -352.8). 30.3*-16.72=-506.6 (obs -504). 
    #   Maybe boundary where linear crosses plateau: x=402.45/16.72=24.07. So for x<24, plateau? But 21.3 is linear-ish.
    #   Wait 21.3->-352.8. If plateau, would be -402.45. It's not. So 21.3 is linear.
    #   So boundary <21.3. Between 2.9 and 21.3. 
    #   Guess: plateau for 0<x<~? Let's say the plateau is a local feature. 
    #   Maybe it's not a plateau but a bump. 1.2 and 2.9 both ~-402.45. Coincidence? Very close values.
    #   Perhaps f(x) = -16.72x for x>threshold, and for 0<x<threshold something ~-402.
    #   Threshold between 2.9 and 21.3. Pick ~10? Unknown. 
    #   Actually maybe the near-zero region is |x|<some and value ~-402 constant. Let's guess boundary at x=10.
    #   Hmm risky. Let me think: 1.2 and 2.9 give nearly identical -402.45. That's a flat region.
    #   Could be f(x) = -402.45 for 0<x<3 (or some range), then linear.
    #   I'll set boundary at x=3 (just above 2.9). For 0<x<3: -402.45. For x>=3: -16.72x.
    #   Check 21.3: -356.2 vs obs -352.8, ok.
    # Negative side: no plateau seen (all negative are linear). -6 is linear.
    out = []
    for x in probe.get("x", []):
        try:
            if x > 0:
                if x < 3:
                    y = -402.45
                else:
                    y = -16.72 * x
            else:
                y = -0.71 * x
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

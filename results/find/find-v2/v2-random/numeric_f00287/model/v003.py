import math

def predict(probe):
    # Observations summary:
    # For x > ~3: y ≈ -16.72x  [E1,E2,E3,E4 large positives]
    #   E4: 93.5->-1562.4 => -16.71; 78.1->-1310.4 => -16.78; 83.2->-1394.4 => -16.76
    #   E3: 58.8->-974.4 => -16.57; 102.1->-1713.6 => -16.78; 47.1->-789.6 => -16.76
    #   Slope ~ -16.72 (E2 exact: 104.5*-16.72=-1747.24). Use -16.72.
    # For x < 0: y ≈ -0.7x  [E1,E2,E3,E4]
    #   E4: -5.9->4.2 => -0.712; -61.3->43.4 => -0.708; -124.4->87.5 => -0.703
    #   E3: -48.6->34.3 => -0.706; -102.2->72.1 => -0.705; -16.9->11.9 => -0.704
    #   Slope ~ -0.705. Use -0.705.
    # For 0 < x < ~? : y ≈ -402.45 constant plateau  [E1: 2.9, E2: 1.2, E4: 12.5]
    #   E4: 12.5->-402.4662 confirms plateau extends to at least 12.5!
    #   E1: 21.3->-352.8 is linear (-16.56*21.3), so boundary between 12.5 and 21.3.
    #   Plateau value ~ -402.45. Boundary: where -16.72x = -402.45 => x=24.07, but 21.3 is linear.
    #   So plateau ends before 21.3. Guess boundary at x=20? Or maybe plateau is |x|<something.
    #   Actually maybe the plateau is a bump: constant -402.45 for 0<x<~15-20, then linear.
    #   Let's estimate: 12.5 plateau, 21.3 linear. Boundary ~ 15-20. Pick 18? 
    #   Hmm, could the plateau be exactly where -16.72x would be less than -402.45? No, that's x<24.
    #   But 21.3 gives -352.8 which is LESS negative than -402.45. So linear at 21.3 gives -356, 
    #   which is less negative than plateau. So plateau is a dip below the line.
    #   Boundary unknown between 12.5 and 21.3. Pick 17 as guess.
    out = []
    for x in probe.get("x", []):
        try:
            if x > 0:
                if x < 17:
                    y = -402.45
                else:
                    y = -16.72 * x
            else:
                y = -0.705 * x
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

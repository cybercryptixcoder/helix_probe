import math

def predict(probe):
    # Model of the black box f(x):
    # Negative side: for x <= -5 (floor(x) <= -5), y = -0.7 * floor(x)  [E1,E2,E3,E5,E7,E8,E9,E11,E12,E13]
    #   E12: at x=-5.1 -> 4.2 = -0.7*(-6); at x=-5.0 -> plateau. So boundary is x <= -5.1? 
    #   Actually -5.1 floor=-6 -> 4.2; -5.0 floor=-5 -> plateau. So linear when floor(x) <= -6.
    # Plateau: -5 <= x < 18.6 approx -> y ≈ -402.3 (noisy constant)  [E4,E6,E8,E10,E12,E13]
    # Positive linear: y = -16.8 * floor(x)  [E1,E3,E5,E6,E9,E10,E11,E13,E14]
    #   E14: 18.6..18.99 -> -302.4 = -16.8*18. So linear begins at x >= 18.6 (floor=18).
    #   E10 had 18.5 -> plateau, 18.9 -> -302.4. So boundary between 18.5 and 18.6.
    #   E6: 18 -> plateau, 19 -> -319.2. Consistent with floor>=18 linear.
    #   So positive linear when floor(x) >= 18, i.e. x >= 18.0? But E6 x=18 -> plateau!
    #   E6 x=18 gave plateau. E14 x=18.6 gave -302.4 (floor 18). So boundary is not floor>=18.
    #   Boundary between 18.5 (plateau) and 18.6 (linear). Use x >= 18.6? 
    #   Hmm but E6 x=18 plateau, E14 18.6 linear. Threshold somewhere in (18.5,18.6].
    #   Best guess: x >= 18.6 -> linear using floor(x). Marked with ?.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        try:
            fx = math.floor(x)
        except Exception:
            ys.append(None)
            continue
        if fx <= -6:
            ys.append(-0.7 * fx)
        elif x >= 18.6:  # ? boundary between 18.5 and 18.6
            ys.append(-16.8 * fx)
        else:
            ys.append(-402.3)
    return {"y": ys}

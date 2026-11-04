import math

def predict(probe):
    # Model of the black box f(x):
    # Negative side: for floor(x) <= -6, y = -0.7 * floor(x)  [E1,E2,E3,E5,E7,E8,E9,E11,E12,E13]
    #   E12: x=-5.1 (floor -6) -> 4.2; x=-5.0 (floor -5) -> plateau. Boundary at floor(x) <= -6.
    # Plateau: -5 <= x < 18.55 approx -> y ≈ -402.3 (noisy constant)  [E4,E6,E8,E10,E12,E13,E16]
    #   E16: 18.55 -> -302.4 (linear); 18.5 -> plateau. So boundary between 18.5 and 18.55.
    # Positive linear: y = -16.8 * floor(x)  [E1,E3,E5,E6,E9,E10,E11,E13,E14,E16]
    #   E14: 18.6..18.99 -> -302.4 = -16.8*18; 19.0 -> -319.2 = -16.8*19. Uses floor(x).
    #   E16: 18.55 -> -302.4 (floor 18). So linear begins at x >= 18.55 (floor 18).
    #   Boundary: x >= 18.55 -> linear using floor(x). (between 18.5 and 18.55)
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
        elif x >= 18.55:  # ? boundary between 18.5 and 18.55
            ys.append(-16.8 * fx)
        else:
            ys.append(-402.3)
    return {"y": ys}

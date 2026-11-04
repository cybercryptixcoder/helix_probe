import math

def predict(probe):
    # Negative side: floor(x) <= -6 -> y = -0.7*floor(x) [E1,E2,E3,E5,E7,E8,E9,E11,E12,E13,E18]
    #   E18: -5.99,-5.5 (floor -6) -> 4.2; -5.01 (floor -6) -> plateau! Wait: -5.01 floor=-6 -> 4.2? observed -402.27.
    #   E18: -5.99 -> 4.2, -5.5 -> 4.2, -5.01 -> -402.27. So boundary is x < -5.5? floor(-5.5)=-6, floor(-5.01)=-6.
    #   Hmm -5.01 gives plateau, so boundary is not floor. E12: -5.1 -> 4.2, -5.0 -> plateau.
    #   So negative linear for x <= -5.1-ish, plateau for x >= -5.0. Boundary between -5.1 and -5.01.
    #   Use x < -5.05 ? Actually -5.01 is plateau, -5.1 is linear. Boundary in (-5.1,-5.01].
    #   y = -0.7*floor(x): -5.1->floor -6 ->4.2 ok; -5.5->floor -6->4.2 ok; -5.99->floor -6->4.2 ok.
    # Plateau: -5.0 <= x < 18.55 -> y ~ -402.3 noisy [E4,E6,E8,E10,E12,E13,E16,E18]
    # Positive linear: x >= 18.55 -> y = -16.8*floor(x) [E14,E16,E17]
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
        if x < -5.05:
            ys.append(-0.7 * fx)
        elif x >= 18.55:
            ys.append(-16.8 * fx)
        else:
            ys.append(-402.3)
    return {"y": ys}

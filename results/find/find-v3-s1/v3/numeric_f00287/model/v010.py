import math

def predict(probe):
    # Negative side: x <= -5.1 -> y = -0.7*floor(x)  [E1,E2,E3,E5,E7,E8,E9,E11,E12,E13,E18,E20,E22,E23]
    #   Boundary: -5.15 -> 4.2 (linear), -5.08 -> plateau [E24]. So boundary in (-5.15,-5.08].
    #   Use x < -5.1 ? -5.15 linear, -5.08 plateau. Boundary between -5.15 and -5.08.
    #   E12: -5.1 -> 4.2 linear, -5.0 -> plateau. So boundary in (-5.1,-5.0].
    #   Combine: -5.15 linear, -5.1 linear, -5.08 plateau. Boundary in (-5.1,-5.08].
    #   Use x <= -5.1 -> linear.
    # Plateau: -5.1 < x < 18.5 -> y ~ -402.3 noisy [E4,E6,E8,E10,E12,E13,E16,E18,E21,E24]
    #   E24: 18.45 -> -402.4671 (plateau), 18.5 -> -402.3158 (plateau), 18.52 -> -302.4 (linear).
    #   So positive boundary in (18.5, 18.52]. Use x <= 18.5 -> plateau.
    # Positive linear: x > 18.5 -> y = -16.8*floor(x) [E14,E16,E17,E22,E23,E24]
    #   E24: 18.52 floor=18 -> -302.4 = -16.8*18. ok.
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
        if x <= -5.1:
            ys.append(-0.7 * fx)
        elif x <= 18.5:
            ys.append(-402.3)
        else:
            ys.append(-16.8 * fx)
    return {"y": ys}

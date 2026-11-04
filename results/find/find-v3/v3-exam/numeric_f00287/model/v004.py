def predict(probe):
    # A: x >= 19: y = -16.8*floor(x) [E2,E5,E7,E8]
    #    E8: 18.5 -> -402.3 (B), 19.0 -> -319.2 = -16.8*19 (A). Boundary at x>=19.
    # B: -5 <= x < 19: y = -402.3 (noisy constant) [E2,E6,E7,E8]
    #    E6: -5.0 -> -402.28 (B), -5.1 -> 4.2 (C). Boundary at x>=-5.
    # C: x < -5: y = -0.7*floor(x) [E1,E2,E4,E5,E6,E7]
    #    E4: -10.1 -> 7.7 = -0.7*(-11)? floor(-10.1)=-11 -> 7.7 ✓
    #        -10.5 -> 7.7 = -0.7*(-11) ✓ ; -9.9 -> 7.0 = -0.7*(-10) ✓
    import math
    xs = probe["x"]
    ys = []
    for x in xs:
        if x < -5:
            ys.append(-0.7 * math.floor(x))
        elif x < 19:
            ys.append(-402.3)
        else:
            ys.append(-16.8 * math.floor(x))
    return {"y": ys}

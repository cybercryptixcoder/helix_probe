import math

def predict(probe):
    # A: x <= -5.1 -> y = -0.7 * floor(x)  [E1,E2,E3,E5,E6,E7,E9]
    #    boundary: -5.1 gives 4.2, -5.09..-5.0 give middle [E6,E10]
    # B: -5.1 < x < 18.52 -> y ≈ -402.4 (noisy constant)  [E2,E4,E8,E10]
    #    upper boundary: 18.51 middle, 18.52 positive [E10]
    # C: x >= 18.52 -> y = -16.8 * floor(x)  [E2,E3,E5,E6,E7,E9,E10]
    out = []
    for x in probe["x"]:
        if x <= -5.1:
            y = -0.7 * math.floor(x)
        elif x < 18.52:
            y = -402.4
        else:
            y = -16.8 * math.floor(x)
        out.append(y)
    return {"y": out}

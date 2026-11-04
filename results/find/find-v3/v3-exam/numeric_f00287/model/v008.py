import math

def predict(probe):
    # Regime A: x < -5: f(x) = -0.7 * floor(x)  [E1,E2,E4,E5,E6,E7,E9]
    # Regime B: -5 <= x < 18.52: flat ~-402.3 (noise)  [E2,E3,E6,E7,E8,E9,E11,E12,E13,E14]
    #   E14: 18.5001,18.505,18.51 flat; 18.52 slope -> boundary in (18.51,18.52]
    # Regime C: x >= 18.52: f(x) = -16.8 * floor(x)  [E1,E2,E3,E5,E6,E8,E9,E10,E12,E13,E14]
    x = probe["x"]
    y = []
    for xi in x:
        if xi < -5:
            y.append(-0.7 * math.floor(xi))
        elif xi < 18.52:
            y.append(-402.3)
        else:
            y.append(-16.8 * math.floor(xi))
    return {"y": y}

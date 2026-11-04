import math

def predict(probe):
    # A: x < 0: y = -0.705*x (linear) [E1-E8, E17-E21]
    # B: 0 <= x < ~18: y = -402.3 (constant plateau) [E1,E2,E4,E5,E6,E7,E21]
    #    E21: 7.1->-402.2972, -3.3->-402.4076, 15.7->-402.2785, -1.4->-402.3651
    #    plateau value ~ -402.3, not exactly constant (slight noise)
    # C: x >= ~18: y = -16.8*x (linear) [E1-E10]
    #    E21: 65.4->-1092.0 => -16.70; 98.3->-1646.4 => -16.75
    #    Slope ~ -16.8. Use -16.8.
    out = []
    for x in probe.get("x", []):
        try:
            if x < 0:
                y = -0.705 * x
            elif x < 18:
                y = -402.3
            else:
                y = -16.8 * x
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

import math

def predict(probe):
    # A: x < 0: y = -0.705*x (linear) [E1-E8]
    # B: 0 < x < ~18: y = -402.45 (constant plateau) [E1,E2,E4,E5,E6,E7]
    # C: x >= ~18: y = -16.8*x (linear) [E1-E10]
    #    E10: 20.4->-336.0 => -16.47; 41.0->-688.8 => -16.80; 28.9->-470.4 => -16.28
    #    127.0->-2133.6 => -16.80; 115.1->-1932.0 => -16.79; 106.7->-1780.8 => -16.69
    #    75.1->-1260.0 => -16.78
    #    Slope is ~ -16.8, not -16.56. Use -16.8.
    out = []
    for x in probe.get("x", []):
        try:
            if x < 0:
                y = -0.705 * x
            elif x < 18:
                y = -402.45
            else:
                y = -16.8 * x
        except Exception:
            y = None
        out.append(y)
    return {"y": out}

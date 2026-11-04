def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 everywhere [E1-E7, E8, E10]
    # Plateau: constant ~7772.9 for x in [97.55, 117.55] [E6, E8, E12, E14]
    #   E14: 97.55 -> plateau (7773.0156), 97.5 -> poly (E8: 1226576.9625)
    #   E14: 117.55 -> plateau (7773.0815), 117.6 -> poly (2145865.3968)
    #   E8: 97.5 -> poly, 98 -> plateau; 117.5 -> plateau, 118 -> poly
    #   Value drifts slightly (~7772.84-7773.10), noise; use 7772.9
    def f(x):
        if 97.55 <= x <= 117.55:
            return 7772.9
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    return {"y": [f(x) for x in probe["x"]]}

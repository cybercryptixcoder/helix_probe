def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 everywhere [E1-E7, E8, E10, E16]
    # Plateau: constant ~7772.9 for x in [97.52, 117.56] [E6, E8, E12, E14, E18, E20]
    #   E20: 97.50 -> poly (1226576.9625), 97.52 -> plateau (7772.8856)
    #   E20: 117.56 -> plateau (7772.9881), 117.58 -> poly (2144776.0727)
    #   E12: 97.6 -> plateau, 117.6 -> poly; E14: 97.55 plateau, 117.55 plateau
    #   Value drifts slightly (~7772.76-7773.13), noise; use 7772.9
    def f(x):
        if 97.52 <= x <= 117.56:
            return 7772.9
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    return {"y": [f(x) for x in probe["x"]]}

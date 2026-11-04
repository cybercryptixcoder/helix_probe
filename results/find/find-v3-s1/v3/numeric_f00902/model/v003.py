def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 everywhere [E1-E7, E8, E10]
    # Plateau: constant ~7772.9 for x in [98, 117.5] [E6, E8]
    #   E8: 97.5 -> poly (1226576.96), 98 -> plateau; 117.5 -> plateau, 118 -> poly
    #   E11: 97.9 -> plateau (7772.8885), so lower bound is <= 97.9
    #   E6: 95 -> poly, 98 -> plateau; so lower bound in (95, 97.9]
    #   Upper: 117.5 plateau, 118 poly
    #   Value drifts slightly (~7772.84-7773.10), noise; use 7772.9
    def f(x):
        if 97.9 <= x <= 117.5:
            return 7772.9
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    return {"y": [f(x) for x in probe["x"]]}

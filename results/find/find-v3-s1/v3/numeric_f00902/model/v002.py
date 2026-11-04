def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 everywhere [E1-E7, E8]
    # Plateau: constant ~7772.9 for x in [98, 117.5] [E6, E8]
    #   E8: 97.5 -> poly (1226576.96), 98 -> plateau; 117.5 -> plateau, 118 -> poly
    #   So plateau is [98, 117.5] (inclusive-ish; 117.5 plateau, 118 poly)
    #   Value drifts slightly (~7772.84-7773.10), noise; use 7772.9
    def f(x):
        if 98 <= x <= 117.5:
            return 7772.9
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    return {"y": [f(x) for x in probe["x"]]}

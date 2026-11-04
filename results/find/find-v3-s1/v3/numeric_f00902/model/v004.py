def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 everywhere [E1-E7, E8, E10]
    # Plateau: constant ~7772.9 for x in [97.6, 117.4] [E6, E8, E12]
    #   E12: 97.3 -> poly (1219087.9991), 97.6 -> plateau (7772.8635)
    #   E12: 117.4 -> plateau (7772.9333), 117.6 -> poly (2145865.3968)
    #   E8: 97.5 -> poly, 98 -> plateau; 117.5 -> plateau, 118 -> poly
    #   Value drifts slightly (~7772.84-7773.10), noise; use 7772.9
    def f(x):
        if 97.6 <= x <= 117.4:
            return 7772.9
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    return {"y": [f(x) for x in probe["x"]]}

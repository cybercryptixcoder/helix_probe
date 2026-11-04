def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 outside anomalous interval [97.6, 117.55]
    # Anomalous interval: f ~ 7772.9 (constant, small noise) [E4, E8, E10, E12]
    # Lower boundary: x=97.5 is cubic (1226576.96), x=97.6 is anomalous (7772.98) [E10, E12]
    # Upper boundary: x=117.55 anomalous (7773.01), x=117.6 cubic (2145865.4) [E12]
    # So interval is [97.6, 117.55]
    def cubic(x):
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    def f(x):
        if 97.6 <= x <= 117.55:
            return 7772.9
        return cubic(x)
    return {"y": [f(x) for x in probe["x"]]}

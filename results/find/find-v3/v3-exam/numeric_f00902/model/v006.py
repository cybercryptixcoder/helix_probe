def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 outside anomalous interval [97.9, 117.5]
    # Anomalous interval: f ~ 7772.9 (constant, small noise) [E4, E8, E10]
    # Lower boundary: x=97.5 is cubic (1226576.96), x=97.9 is anomalous (7772.96) [E10]
    # Upper boundary: x=117.5 anomalous (7772.9982), x=118 cubic (2167729.4) [E6]
    # So interval is [97.9, 117.5] (boundary between 97.5 and 97.9) [E10, E6]
    def cubic(x):
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    def f(x):
        if 97.9 <= x <= 117.5:
            return 7772.9
        return cubic(x)
    return {"y": [f(x) for x in probe["x"]]}

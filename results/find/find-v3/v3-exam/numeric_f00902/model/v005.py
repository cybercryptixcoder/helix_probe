def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 outside the anomalous interval [E2, E3, E5]
    # Anomalous interval: f ~ 7772.9 (roughly constant, small noise) [E4]
    # Lower boundary: x=97 is cubic (1207911.8), x=99 is anomalous (7772.98) [E4]
    # Upper boundary: x=117.5 anomalous (7772.9982), x=118 cubic (2167729.4) [E6]
    # So interval is [98, 117.5] (boundary between 117.5 and 118) [E4, E6]
    def cubic(x):
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    def f(x):
        if 98 <= x <= 117.5:
            return 7772.9
        return cubic(x)
    return {"y": [f(x) for x in probe["x"]]}

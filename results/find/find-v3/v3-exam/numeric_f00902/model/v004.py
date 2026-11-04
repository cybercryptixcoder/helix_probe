def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 outside the anomalous interval [E1, E2]
    # Anomalous interval: f ~ 7772.9 (roughly constant, small noise) [E4]
    # Lower boundary: x=97 is cubic (1207911.8), x=99 is anomalous (7772.98) [E4]
    # Upper boundary: x=115 anomalous (7772.71), x=119.5 cubic (2251041.6) [E4, E5]
    # So interval is roughly [98, ~117]; guess [98, 117] [E4, E5]?
    def cubic(x):
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    def f(x):
        if 98 <= x <= 117:
            return 7772.9
        return cubic(x)
    return {"y": [f(x) for x in probe["x"]]}

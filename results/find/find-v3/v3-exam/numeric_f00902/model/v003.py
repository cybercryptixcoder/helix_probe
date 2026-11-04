def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 outside the anomalous interval [E1, E2, E3]
    # Anomalous interval: f ~ 7772.9 (roughly constant, small noise) for x in [99, 115] [E4]
    # Boundary: x=97 is cubic (1207911.8), x=99 is anomalous (7772.98) [E4]
    # Boundary: x=115 is anomalous (7772.71), x=123.6 is cubic [E3, E4]
    # Values inside are noisy around ~7772.9, spread ~0.5 [E4]
    # Exact upper boundary unknown between 115 and 123.6; guess 120 [E3, E4]?
    def cubic(x):
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    def f(x):
        if 99 <= x <= 120:
            return 7772.9
        return cubic(x)
    return {"y": [f(x) for x in probe["x"]]}

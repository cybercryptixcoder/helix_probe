def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 outside the anomalous interval [E1-E19]
    # Anomalous interval: f ~ 7772.9 (constant, small noise) [E4, E8, E10, E12, E16, E18]
    # Lower boundary: x=97.575 is anomalous, x=97.55 is cubic [E20]
    # Upper boundary: x=117.55 anomalous, x=117.575 cubic [E20]
    # So interval is [97.575, 117.55] (sharp transitions, no transition zone) [E20]
    def cubic(x):
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    def f(x):
        if 97.575 <= x <= 117.55:
            return 7772.9
        return cubic(x)
    return {"y": [f(x) for x in probe["x"]]}

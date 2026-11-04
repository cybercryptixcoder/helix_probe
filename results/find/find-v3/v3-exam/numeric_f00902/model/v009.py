def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 outside the anomalous interval [E1-E19]
    # Anomalous interval: f ~ 7772.9 (constant, small noise) [E4, E8, E10, E12, E16, E18]
    # Lower boundary: x<=97.575 is anomalous; x>=97.56? No: 97.575 anomalous, 97.55 cubic [E20, E22]
    #   E22: 97.55,97.555,97.56,97.565,97.57,97.575 ALL anomalous -> lower cutoff is <=97.55
    #   E20: 97.55 anomalous, 97.575 anomalous, 97.6 anomalous... wait E20 97.55 anomalous
    #   E20: 97.55 -> 7773.02 (anomalous). So lower boundary is below 97.55.
    #   E10: 97.5 -> cubic (1228453.98). So lower boundary in (97.5, 97.55].
    # Upper boundary: 117.56 anomalous, 117.565 cubic [E22]
    #   E22: 117.55,117.555,117.56 anomalous; 117.565,117.57,117.575 cubic
    #   So upper cutoff in (117.56, 117.565].
    def cubic(x):
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    def f(x):
        if 97.5 < x <= 117.56:
            return 7772.9
        return cubic(x)
    return {"y": [f(x) for x in probe["x"]]}

def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6, single cubic everywhere [E1, E2]
    return {"y": [1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6 for x in probe["x"]]}

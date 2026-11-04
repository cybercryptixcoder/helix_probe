def predict(probe):
    # f(x) ≈ 2.7 * x  [E1: all 10 points near 2.7x; residuals up to ~15 suggest noise or
    #                  a slight nonlinearity I can't pin down from one experiment]
    return {"y": [2.7 * x for x in probe["x"]]}

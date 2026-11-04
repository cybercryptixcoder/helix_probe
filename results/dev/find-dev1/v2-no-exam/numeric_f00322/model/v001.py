def predict(probe):
    # f(x) = 53 for all tested x in [-128,128] [E1]
    # No sign/magnitude/region variation observed across full domain [E1]
    return {"y": [53.0 for _ in probe["x"]]}

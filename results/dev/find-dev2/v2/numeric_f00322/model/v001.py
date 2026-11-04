def predict(probe):
    # f returns 53.0 for every tested x in [-128, 128] [E1]
    # No evidence of any region or special interval; constant everywhere probed [E1]
    return {"y": [53.0 for _ in probe["x"]]}

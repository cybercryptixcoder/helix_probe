def predict(probe):
    # f returns 0 for all tested inputs [E1]
    # No evidence of any nonzero output; assume constant zero everywhere (?)
    return {"y": [0.0 for _ in probe["x"]]}

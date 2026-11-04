def predict(probe):
    # f(x) returns 0 (signed zero) for all tested x in [-128,128] [E1]
    # No evidence of any nonzero output or undefined region yet [E1]
    # Best guess: constant zero function; sign of zero may vary but value is 0
    return {"y": [0.0 for _ in probe["x"]]}

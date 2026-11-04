def predict(probe):
    # y = x - 39.5 [E1]; offsets ranged -39.0..-39.9, consistent with constant shift
    # No evidence of a special region yet [?]
    return {"y": [x - 39.5 for x in probe["x"]]}

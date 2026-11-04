def predict(probe):
    # f(x) = x + "xI" for all tested inputs [E1]
    # No other transformation observed; suffix appended verbatim [E1]
    return {"outputs": [x + "xI" for x in probe["inputs"]]}

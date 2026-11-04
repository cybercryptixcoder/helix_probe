def predict(probe):
    # f(x) = x + "xI" for every input seen [E1]
    # No other transformation observed; append "xI" to each input.
    return {"outputs": [s + "xI" for s in probe["inputs"]]}

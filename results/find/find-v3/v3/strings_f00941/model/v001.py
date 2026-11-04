def predict(probe):
    # f(x) = x + "ny" for every input seen [E1]
    # No transformation of the input itself is observed; it is simply appended [E1]
    return {"outputs": [x + "ny" for x in probe["inputs"]]}

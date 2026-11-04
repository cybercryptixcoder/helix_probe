def predict(probe):
    # The box appends "ny" to every input string [E1]
    # No case change, no reversal, spaces/digits/symbols preserved [E1]
    return {"outputs": [s + "ny" for s in probe["inputs"]]}

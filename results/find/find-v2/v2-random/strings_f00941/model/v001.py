def predict(probe):
    # Appends "ny" to every input string [E1]
    # No other transformation observed; applies regardless of content,
    # case, spaces, digits, or symbols [E1]
    return {"outputs": [s + "ny" for s in probe["inputs"]]}

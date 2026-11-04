def predict(probe):
    # Appends "ny" to every input string [E1]
    # No other transformation observed; applies to digits, spaces, mixed case [E1]
    return {"outputs": [x + "ny" for x in probe["inputs"]]}

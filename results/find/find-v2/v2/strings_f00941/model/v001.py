def predict(probe):
    # Appends "ny" to every input string [E1]
    # No other transformation observed; applies to all characters/cases/spaces [E1]
    return {"outputs": [s + "ny" for s in probe["inputs"]]}

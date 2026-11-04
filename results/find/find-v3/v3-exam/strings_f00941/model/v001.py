def predict(probe):
    # Appends "ny" to every input string [E1]
    return {"outputs": [s + "ny" for s in probe["inputs"]]}

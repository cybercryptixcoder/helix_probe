def predict(probe):
    # Appends "T" to every input string [E1]
    return {"outputs": [s + "T" for s in probe["inputs"]]}

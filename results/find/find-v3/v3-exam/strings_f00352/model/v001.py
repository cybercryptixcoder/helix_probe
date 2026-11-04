def predict(probe):
    # Appends "T" to every input [E1]
    return {"outputs": [s + "T" for s in probe["inputs"]]}

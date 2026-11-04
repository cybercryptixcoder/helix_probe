def predict(probe):
    # Appends "T" to every input [E1]
    return {"outputs": [x + "T" for x in probe["inputs"]]}

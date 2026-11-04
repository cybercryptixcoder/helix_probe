def predict(probe):
    # Appends "T" to every input, unchanged otherwise [E1]
    return {"outputs": [x + "T" for x in probe["inputs"]]}

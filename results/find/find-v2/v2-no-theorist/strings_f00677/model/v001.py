def predict(probe):
    # Appends the literal string "xI" to every input [E1]
    return {"outputs": [s + "xI" for s in probe["inputs"]]}

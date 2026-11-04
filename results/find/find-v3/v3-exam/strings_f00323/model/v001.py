def predict(probe):
    # Reverses the whole string [E1: all 6 outputs are exact reversals]
    return {"outputs": [s[::-1] for s in probe["inputs"]]}

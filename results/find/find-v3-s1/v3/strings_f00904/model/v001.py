def predict(probe):
    # f reverses the entire string, character by character [E1]
    # Case is preserved as-is; spaces and symbols are just characters [E1]
    return {"outputs": [s[::-1] for s in probe["inputs"]]}

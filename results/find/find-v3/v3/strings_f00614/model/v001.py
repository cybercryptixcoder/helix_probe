def predict(probe):
    # Removes all spaces, then appends 'F' [E1]
    # (Case preserved, digits/symbols preserved) [E1]
    return {"outputs": [s.replace(" ", "") + "F" for s in probe["inputs"]]}

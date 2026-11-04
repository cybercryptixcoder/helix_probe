def predict(probe):
    # Removes spaces and appends "F" [E1]
    # All other characters (digits, letters, case) preserved unchanged [E1]
    return {"outputs": [x.replace(" ", "") + "F" for x in probe["inputs"]]}

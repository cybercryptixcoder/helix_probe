def predict(probe):
    # Removes all spaces from input [E1]
    # Other characters (letters, digits, case) unchanged [E1]
    return {"outputs": [s.replace(" ", "") for s in probe["inputs"]]}

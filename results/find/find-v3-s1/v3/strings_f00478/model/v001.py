def predict(probe):
    # Removes all spaces from the input string [E1]
    # Other characters (letters, digits, symbols, case) are preserved unchanged [E1]
    return {"outputs": [s.replace(" ", "") for s in probe["inputs"]]}

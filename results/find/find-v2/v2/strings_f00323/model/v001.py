def predict(probe):
    # Reverses the string [E1: "abc123"->"321cba", "Zebra"->"arbeZ"]
    # Palindromes unchanged [E1: "level"->"level"]
    # Reversal is per whole string including spaces [E1: " Zebralower"->"rewolarbeZ"]
    return {"outputs": [s[::-1] for s in probe["inputs"]]}

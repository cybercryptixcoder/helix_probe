def predict(probe):
    # Removes all spaces from the input string [E1: "two words"->"twowords", "a b c"->"abc", "abc def ghi"->"abcdefghi"]
    # No other transformation observed yet; case, digits, symbols untested [?]
    return {"outputs": [s.replace(" ", "") for s in probe["inputs"]]}

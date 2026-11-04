def predict(probe):
    # Removes all spaces from input [E1: "two words"->"twowords", "a b c"->"abc"]
    # Appends "F" to the result [E1: all outputs end in F]
    # Other characters (case, digits, punctuation) pass through unchanged [E1]
    return {"outputs": [s.replace(" ", "") + "F" for s in probe["inputs"]]}

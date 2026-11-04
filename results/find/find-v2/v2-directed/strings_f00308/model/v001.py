def predict(probe):
    # Removes all spaces from input [E1: "two words"->"twowords", "a b c"->"abc", " "->""]
    # Everything else passes through unchanged: case preserved, digits/symbols kept [E1]
    return {"outputs": [s.replace(" ", "") for s in probe["inputs"]]}

def predict(probe):
    # Reverses the whole string, then removes all spaces [E1, E2]
    # E2: "hello world"->"dlrowolleh", "a b c"->"cba", " leading"->"gnidael"
    return {"outputs": [s[::-1].replace(" ", "") for s in probe["inputs"]]}

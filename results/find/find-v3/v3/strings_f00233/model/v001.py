def predict(probe):
    # Reverse the string, then swap case of each character [E1, E2]
    # Digits and punctuation are unchanged by case swap [E2]
    return {"outputs": [s[::-1].swapcase() for s in probe["inputs"]]}

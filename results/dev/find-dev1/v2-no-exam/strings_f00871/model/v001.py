def predict(probe):
    # f reverses the input string, then appends "I" [E1]
    # "" -> "I", "a" -> "aI", "ab" -> "baI", "Hello" -> "olleHI" [E1]
    # Case, digits, spaces, punctuation all preserved, just reversed [E1]
    return {"outputs": [s[::-1] + "I" for s in probe["inputs"]]}

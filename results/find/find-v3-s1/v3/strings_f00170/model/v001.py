def predict(probe):
    # Model: output = "k" + reverse(input)  [E1, E2]
    # The leading "k" is a constant prefix; the rest is the full string reversed,
    # preserving case, spaces, digits, and punctuation exactly.
    return {"outputs": ["k" + s[::-1] for s in probe["inputs"]]}

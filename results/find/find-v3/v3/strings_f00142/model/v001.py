def predict(probe):
    # Each char shifted +5 in ASCII, then "W" appended [E1]
    # Works for letters, digits, spaces, symbols [E1]
    return {"outputs": ["".join(chr(ord(c) + 5) for c in s) + "W" for s in probe["inputs"]]}

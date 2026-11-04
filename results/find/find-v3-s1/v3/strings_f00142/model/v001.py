def predict(probe):
    # Shift every character +5 in ASCII, then append "W" [E1]
    # Works for letters, spaces, digits, symbols uniformly [E1]
    return {"outputs": ["".join(chr(ord(c) + 5) for c in s) + "W" for s in probe["inputs"]]}

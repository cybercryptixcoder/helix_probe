def predict(probe):
    # Every character is shifted +5 in ASCII (letters, digits, spaces, punctuation all shift) [E1]
    # A literal "W" is appended to the end of the shifted string [E1]
    return {"outputs": ["".join(chr(ord(c) + 5) for c in s) + "W" for s in probe["inputs"]]}

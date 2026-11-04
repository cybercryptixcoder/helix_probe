def predict(probe):
    # Every character is shifted +8 in ASCII [E1]
    # e.g. 'a'->'i', 'Z'->'b', ' '->'(', '1'->'9' [E1]
    # Applies uniformly to letters, digits, spaces, symbols [E1]
    return {"outputs": ["".join(chr(ord(c) + 8) for c in s) for s in probe["inputs"]]}

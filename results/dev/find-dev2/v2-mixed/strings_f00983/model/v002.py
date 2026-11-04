def predict(probe):
    # Every character is shifted +8 in ASCII [E1, E2]
    # Exception: input 't' is dropped entirely (produces no output char) [E1, E3]
    return {"outputs": ["".join(chr(ord(c) + 8) for c in s if c != "t") for s in probe["inputs"]]}

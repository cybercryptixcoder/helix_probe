def predict(probe):
    # First char: letter shifted +1 (a->b, Z->A, M->N); non-letter unchanged [E1, E2]
    # Everything after first char: unchanged [E1, E2]
    # Then append 'y' to the whole result [E1, E2]
    # Note: "test case " -> "uest case y" = shift first, keep rest incl. trailing space, append y
    #       "  " -> "  y" (no shift since space), append y
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c)-97+1)%26+97)
        if 'A' <= c <= 'Z':
            return chr((ord(c)-65+1)%26+65)
        return c
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append("y")  # ? empty string: append y
            continue
        out.append(shift(s[0]) + s[1:] + "y")
    return {"outputs": out}

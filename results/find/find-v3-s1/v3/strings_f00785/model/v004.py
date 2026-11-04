def predict(probe):
    # First char: letter shifted +1 (a->b, Z->A); non-letter unchanged [E1, E2]
    # Everything after first char: unchanged [E1, E2, E3]
    # Append 'y' to the whole result [E1, E2, E3]
    # Exception: if the ORIGINAL string ends in 'y', do NOT append [E4, E6]
    #   "x y" -> "y y" (orig ends y, no append) [E4]
    #   "x" -> "yy" (orig 'x' doesn't end y, shift->'y', append -> 'yy') [E6]
    #   "y" -> "z" (orig ends y, no append) [E6]
    #   "zx" -> "axy" (orig ends x, append) [E6]
    #   "w" -> "xy" (orig 'w' doesn't end y, shift->'x', append -> 'xy') [E6]
    #   "xyz" -> "yyzy" (orig ends z, append) [E6]
    # Empty string -> "y" [E2]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c)-97+1)%26+97)
        if 'A' <= c <= 'Z':
            return chr((ord(c)-65+1)%26+65)
        return c
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append("y")
            continue
        r = shift(s[0]) + s[1:]
        if not s.endswith("y"):
            r += "y"
        out.append(r)
    return {"outputs": out}

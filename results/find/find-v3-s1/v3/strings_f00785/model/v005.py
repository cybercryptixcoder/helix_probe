def predict(probe):
    # First char: if a letter, shift +1 (a->b, Z->A); non-letter unchanged [E1,E2,E10]
    # Everything after first char: unchanged [E1,E2,E3]
    # Append 'y' to the whole result [E1,E2,E3]
    # Exception: if the ORIGINAL string ends in 'y' (lowercase only), do NOT append [E4,E6,E8]
    #   uppercase 'Y' does NOT suppress the append [E12]
    # Empty string -> "y" [E2]
    # Non-ASCII letters: shift by +1 in Unicode code point [E12]
    #   é->ê, ü->ý, Å->Æ (note: Å is U+00C5, +1 = U+00C6 = Æ) [E12]
    #   ï unchanged (not first char) [E12]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c)-97+1)%26+97)
        if 'A' <= c <= 'Z':
            return chr((ord(c)-65+1)%26+65)
        # Non-ASCII letter: shift by +1 in code point [E12]
        if c.isalpha():
            return chr(ord(c)+1)
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

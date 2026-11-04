def predict(probe):
    # First letter: shifted up by 1 (a->b, H->I, Z->A, space stays) [E1, E2]
    # Rest of string: unchanged [E1, E2, E3]
    # Append 'y' at the end [E1, E2, E3]
    # Suppress appended 'y' only if the ORIGINAL string ends in 'y' [E4, E8]
    #   (E8: "y"->"z" no append; "x"->"yy" append since orig doesn't end in y)
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c)-ord('a')+1)%26+ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c)-ord('A')+1)%26+ord('A'))
        return c
    out = []
    for s in probe["inputs"]:
        if s == "":
            out.append("y")
            continue
        r = shift(s[0]) + s[1:]
        if not s.endswith("y"):
            r += "y"
        out.append(r)
    return {"outputs": out}

def predict(probe):
    # First character: shift +1 in alphabet, wrapping within case [E1, E2, E3]
    #   a->b, l->m, H->I, b->c, Z->A, x->y, A->B, z->a
    # Non-letters at position 0 unchanged (space/digit preserved) [E1, E4]
    # Rest of string unchanged [E1, E2, E3]
    # Append 'y' to every output [E1, E2, E3]
    # BUT: if the ORIGINAL input already ends with 'y', do NOT append another 'y' [E3, E4]
    #   E4: "y"->"z" (shifted to z, no append since input ended in y)
    #       "yy"->"zy" (shift first y->z, rest "y", no append)
    #       "ay"->"by" (input ends y, no append)
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 1) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 1) % 26 + ord('A'))
        return c
    out = []
    for s in probe.get("inputs", []):
        if not s:
            out.append("y")
            continue
        body = shift(s[0]) + s[1:]
        if s.endswith("y"):
            out.append(body)
        else:
            out.append(body + "y")
    return {"outputs": out}

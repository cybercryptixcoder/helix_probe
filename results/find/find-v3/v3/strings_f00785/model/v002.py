def predict(probe):
    # First character: shift +1 in alphabet, wrapping within case [E1, E2, E3]
    #   a->b, l->m, H->I, b->c, Z->A, x->y, A->B, z->a
    # Non-letters at position 0 unchanged (space preserved) [E1]
    # Rest of string unchanged [E1, E2, E3]
    # Append 'y' to every output [E1, E2, E3]
    # BUT: if the input already ends with 'y', do NOT append another 'y' [E3: "lazy"->"mazy"]
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
        if body.endswith("y"):
            out.append(body)
        else:
            out.append(body + "y")
    return {"outputs": out}

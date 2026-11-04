def predict(probe):
    # Every output = transformed input + "JTQL" suffix [E1]
    # First char: a->y, l->j, H->F, b->z, Z->X (shift back by 2 in alphabet) [E1]
    #   'a'->'y', 'l'->'j', 'H'->'F', 'b'->'z', 'Z'->'X' all = -2 [E1]
    # Remaining chars unchanged [E1]
    # Space-leading input " Zebralower" unchanged (first char is space, not letter) [E1]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
        return c
    out = []
    for s in probe.get("inputs", []):
        if s:
            out.append(shift(s[0]) + s[1:] + "JTQL")
        else:
            out.append("JTQL")
    return {"outputs": out}

def predict(probe):
    # Each character is shifted +1 in the alphabet, case preserved [E1]
    #   abc123 -> cbc123? No: a->c is +2, b->c is +1... check.
    # Actually: abc123 -> cbc123: a->c (+2), b->c (+1), c->1? no c stays? c->c.
    # level -> nevel: l->n (+2), e->e, v->v, e->e, l->l
    # Zebralower -> Bebralower: Z->B (+2 wrap), e->e...
    # Hello World function lazy -> JelloWorldfunctionlazy: H->J (+2), rest same, spaces removed
    # bananaUPPER -> dananaUPPER: b->d (+2)
    # Zebra -> Bebra: Z->B (+2)
    # So: first character shifted +2 (wrap, case preserved), spaces removed, rest unchanged.
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
        return c
    out = []
    for s in probe.get("inputs", []):
        s2 = s.replace(" ", "")
        if s2:
            s2 = shift(s2[0]) + s2[1:]
        out.append(s2)
    return {"outputs": out}

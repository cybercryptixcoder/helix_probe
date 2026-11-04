def predict(probe):
    # Shift FIRST character of string by +2 in alphabet, case preserved, wrap [E1,E2,E3]
    #   a->c, l->n, H->J, b->d, Z->B, E->G, t->v, f->h, w->y, r->t [E1,E2,E3]
    # Trailing whitespace is stripped from the result [E2 "banana data banana "->"danana data banana",
    #   E3 "Example "->"Gxample", "banana a data "->"danana a data"]
    # Leading space preserved (non-letter, unchanged) [E1 " Zebralower"]
    # Non-letter first char left unchanged
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
        return c
    out = []
    for s in probe.get("inputs", []):
        if s:
            out.append((shift(s[0]) + s[1:]).rstrip())
        else:
            out.append(s)
    return {"outputs": out}

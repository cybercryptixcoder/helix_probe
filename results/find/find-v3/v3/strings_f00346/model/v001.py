def predict(probe):
    # Rule: first character of each string is shifted +1 in the alphabet [E1]
    #   'a'->'b'? No: "abc123"->"cbc123" (a->c, +2); "level"->"nevel" (l->n, +2);
    #   " Zebralower"->"Bebralower" (space->B? no...). Let's recheck.
    #   "abc123" -> "cbc123": a->c (+2)
    #   "level"  -> "nevel": l->n (+2)
    #   " Zebralower" -> "Bebralower": ' '->'B'? That's not +2. But maybe leading space is dropped?
    #   Actually " Zebralower" has leading space; output "Bebralower" = Z->B (+2), space dropped.
    #   "Hello World function lazy" -> "JelloWorldfunctionlazy": H->J (+2), spaces removed.
    #   "bananaUPPER" -> "dananaUPPER": b->d (+2)
    #   "Zebra" -> "Bebra": Z->B (+2, wrap)
    # So: remove all spaces, then shift first char +2 (wrapping in alphabet, preserving case).
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
        return c
    out = []
    for s in probe["inputs"]:
        t = s.replace(" ", "")
        if t:
            t = shift(t[0]) + t[1:]
        out.append(t)
    return {"outputs": out}

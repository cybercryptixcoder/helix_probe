def predict(probe):
    # Beliefs:
    # - Only the LAST character is shifted [E2,E3,E4]
    # - Lowercase a-y -> next, z -> a [E2,E4]
    # - Uppercase A-Y -> next, Z -> A [E2,E4]
    # - Non-letters unchanged [E2,E4]
    # - Any uppercase 'R' is DELETED, wherever it appears [E6]
    #     "R"->"", "eR"->"e", "ZebraR"->"Zebra", "HERO"->"HEO", "ER"->"E"
    #     (E6: "R"->"", "eR"->"f", "ZebraR"->"Zebrb", "HERO"->"HEP")
    # - Deletion happens BEFORE the last-char shift [E6: "eR"->"e"->"f"]
    # - Lowercase 'r' is NOT deleted [E6: "er"->"es", "zero"->"zerp", "Error"->"Erros"]
    #   Wait: "Error"->"Erros": E,r,r,o,r -> E,r,r,o,s. No uppercase R. Good.
    #   "zero"->"zerp": no uppercase R. Good.
    # - "ER"->"F": delete R -> "E", shift E->F [E6]
    # - "Er"->"Es": no uppercase R, shift r->s [E6]
    # - "HERO"->"HEP": delete R -> "HEO", shift O->P [E6]
    # - "ZebraR"->"Zebrb": delete R -> "Zebra", shift a->b [E6]
    # - "R"->"": delete R -> "", empty stays empty [E6]
    # - "eR"->"f": delete R -> "e", shift e->f [E6]
    # - "midUPPERend"->"midUPPEene": delete R -> "midUPPEend", shift d->e [E4]
    # - "bananaUPPER"->"bananaUPPF": delete R -> "bananaUPPE", shift E->F [E1]
    
    def shift(c):
        if 'a' <= c <= 'z':
            return 'a' if c == 'z' else chr(ord(c)+1)
        if 'A' <= c <= 'Z':
            return 'A' if c == 'Z' else chr(ord(c)+1)
        return c
    
    out = []
    for s in probe.get("inputs", []):
        if not s:
            out.append(s)
            continue
        # Delete every uppercase 'R' [E6]
        t = s.replace("R", "")
        if not t:
            out.append(t)
            continue
        out.append(t[:-1] + shift(t[-1]))
    return {"outputs": out}

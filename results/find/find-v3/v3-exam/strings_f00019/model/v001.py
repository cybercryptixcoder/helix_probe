def predict(probe):
    # Observations from E1:
    #   "abc123" -> "abc123" (unchanged)
    #   "level" -> "levem"  (last char l->m)
    #   " Zebralower" -> " Zebralowes" (last r->s)
    #   "Hello World function lazy" -> "Hello World function lazz" (last y->z)
    #   "bananaUPPER" -> "bananaUPPES" (last R->S)
    #   "Zebra" -> "Zebrb" (last a->b)
    # Pattern: the LAST character is incremented by one (next char in ASCII).
    # "abc123" ends in '3' -> would be '4', but observed unchanged.
    # Hypothesis: only letters are incremented; digits/symbols unchanged.
    #   'l'->'m', 'r'->'s', 'y'->'z', 'R'->'S', 'a'->'b' all fit.
    #   '3' stays '3' fits "digits unchanged".
    # Edge: 'z'/'Z' wrap? Unknown. Guess: wrap to 'a'/'A'? Marked with "?".
    def inc(ch):
        if 'a' <= ch <= 'y':
            return chr(ord(ch) + 1)
        if ch == 'z':
            return 'a'  # ? wrap
        if 'A' <= ch <= 'Y':
            return chr(ord(ch) + 1)
        if ch == 'Z':
            return 'A'  # ? wrap
        return ch
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append(s)
        else:
            out.append(s[:-1] + inc(s[-1]))
    return {"outputs": out}

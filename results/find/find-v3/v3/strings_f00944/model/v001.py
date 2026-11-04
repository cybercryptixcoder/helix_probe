def predict(probe):
    # Last character is shifted +1 in ASCII [E1, E2]
    #   'level'->'levem', 'Zebra'->'Zebrb', 'cat'->'cau', 'quiz'->'quia'
    #   'zzz'->'zza' (z wraps to a), 'aZ'->'aA' (Z wraps to A)
    # All other characters pass through unchanged [E1, E2]
    #   'abc123'->'abc123' (last char '3'->'4'? no: observed 'abc123')
    #   Wait: 'abc123'->'abc123' means last char unchanged when digit.
    #   ' Zebralower'->' Zebralowes' (r->s), 'Hello World function lazy'->'...lazz' (y->z)
    # So shift applies only to letters; digits/symbols unchanged [E1]
    def shift(ch):
        if 'a' <= ch <= 'y':
            return chr(ord(ch) + 1)
        if ch == 'z':
            return 'a'
        if 'A' <= ch <= 'Y':
            return chr(ord(ch) + 1)
        if ch == 'Z':
            return 'A'
        return ch
    out = []
    for s in probe.get("inputs", []):
        if not s:
            out.append(s)
        else:
            out.append(s[:-1] + shift(s[-1]))
    return {"outputs": out}

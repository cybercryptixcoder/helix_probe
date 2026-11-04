def predict(probe):
    # 'a' -> 'c', 'A' -> 'C': lowercase/uppercase letters shift +2 [E1]
    # 'b' -> 'b'? No: "ab"->"cb" means a->c, b->b. So b unchanged? [E1]
    # Actually "ab"->"cb": only first char shifted. Hmm.
    # "AB"->"CB": A->C, B->B. Only first char shifted +2.
    # "aB"->"cB": a->c, B->B. Only first char shifted.
    # "a b"->"c b": a->c, rest unchanged.
    # So: only the FIRST character is shifted +2 if it's a letter.
    # digits, symbols, spaces, empty unchanged [E1]
    def shift(ch):
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') + 2) % 26 + ord('A'))
        return ch
    out = []
    for s in probe.get("inputs", []):
        if s:
            out.append(shift(s[0]) + s[1:])
        else:
            out.append(s)
    return {"outputs": out}

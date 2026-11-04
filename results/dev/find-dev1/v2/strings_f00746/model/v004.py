def predict(probe):
    # First char shifted +2 if ASCII letter, case preserved, wrapping [E1-E4, E8]
    # Non-letter first char: no shift [E1, E3, E4]
    # Only the first character is ever shifted [E2-E5]
    # Non-ASCII letters DO get shifted +2 (é->ë, ñ->ó) [E8]
    # ALL trailing whitespace stripped from output (spaces, tabs, \n, \r) [E5, E6]
    # Leading and interior whitespace preserved [E2, E3, E5, E7]
    # Empty / all-whitespace strings become empty [E1, E6]
    def shift(ch):
        o = ord(ch)
        if 'a' <= ch <= 'z':
            return chr((o - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= ch <= 'Z':
            return chr((o - ord('A') + 2) % 26 + ord('A'))
        # Non-ASCII letters: shift +2 in codepoint space (é->ë, ñ->ó) [E8]
        if ch.isalpha():
            return chr(o + 2)
        return ch
    out = []
    for s in probe.get("inputs", []):
        if s:
            out.append((shift(s[0]) + s[1:]).rstrip())
        else:
            out.append(s)
    return {"outputs": out}

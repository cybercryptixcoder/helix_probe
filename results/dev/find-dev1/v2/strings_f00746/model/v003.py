def predict(probe):
    # First char shifted +2 if letter (case preserved) [E1-E4]
    # Non-letter first char: no shift [E1, E3, E4]
    # Only the first character is ever shifted [E2-E5]
    # ALL trailing whitespace stripped from output (spaces, tabs, \n, \r) [E5, E6]
    # Leading and interior whitespace preserved [E2, E3, E5]
    # Empty / all-whitespace strings become empty [E1, E6]
    def shift(ch):
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') + 2) % 26 + ord('A'))
        return ch
    out = []
    for s in probe.get("inputs", []):
        if s:
            out.append((shift(s[0]) + s[1:]).rstrip())
        else:
            out.append(s)
    return {"outputs": out}

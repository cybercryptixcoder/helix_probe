def predict(probe):
    # Every character is shifted by a fixed Caesar-like offset [E1]:
    #   'a'->'c', 'A'->'C', '1'->'5', '!'->'%', ' '->'$'
    # Offsets: lowercase +2, uppercase +2, digit +4, '!' +4, space +4.
    # Empty string maps to empty string [E1].
    # Hypothesis (?): shift depends on character class; unknown classes unchanged.
    def shift(ch):
        o = ord(ch)
        if 'a' <= ch <= 'z':
            return chr((o - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= ch <= 'Z':
            return chr((o - ord('A') + 2) % 26 + ord('A'))
        if '0' <= ch <= '9':
            return chr((o - ord('0') + 4) % 10 + ord('0'))
        if ch == '!':
            return '%'
        if ch == ' ':
            return '$'
        return ch
    return {"outputs": ["".join(shift(c) for c in s) for s in probe["inputs"]]}

def predict(probe):
    # First character is shifted +2 if it's an ASCII letter, wrapping within
    #   its own case's alphabet [E1,E2,E3,E9]
    #   "xyz"->"zyz", "z"->"b", "Z"->"B", "y"->"a", "Y"->"A" [E2,E9]
    # Non-letter first char is unchanged [E1,E3,E7]
    # Rest of the string is unchanged [E1,E2,E3,E7,E8]
    # Trailing whitespace is stripped (after shift) [E4,E5]
    # Whitespace-only strings become "" [E1,E3,E4]
    # Non-ASCII letters are shifted +2 by codepoint (no wrap) [E6]
    def shift(ch):
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') + 2) % 26 + ord('A'))
        if ch.isalpha():
            return chr(ord(ch) + 2)
        return ch
    out = []
    for s in probe["inputs"]:
        if s.strip() == "":
            out.append("")
        else:
            out.append((shift(s[0]) + s[1:]).rstrip())
    return {"outputs": out}

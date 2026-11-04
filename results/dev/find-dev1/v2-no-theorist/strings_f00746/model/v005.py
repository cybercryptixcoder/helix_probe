def predict(probe):
    # First character is shifted +2 if it's an ASCII letter, wrapping [E1,E2,E3]
    #   "xyz"->"zyz", "XYZ"->"ZYZ", "z"->"b", "Z"->"B" [E2]
    # Non-letter first char is unchanged [E1,E3]
    # Rest of the string is unchanged [E1,E2,E3]
    # Trailing whitespace is stripped (after shift) [E4,E5]
    # Whitespace-only strings become "" [E1,E3,E4]
    # Non-ASCII letters are ALSO shifted +2 (Unicode-aware) [E6]
    #   "é"->"ë", "éa"->"ëa", "ß"->"á" (ß+2=á? actually ß=U+00DF, +2=U+00E1=á) [E6]
    #   "αβ"->"γβ" (α=U+03B1, +2=U+03B3=γ) [E6]
    # So shift applies to any Unicode alphabetic char, by codepoint +2 [E6]
    def shift(ch):
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

def predict(probe):
    # First character is shifted +2 (letters, wrapping) [E1,E2,E3]
    # Rest of the string is unchanged [E1,E2,E3]
    # Non-letter first char is unchanged [E1: "1"->"1", "!"->"!", E3: "1abc","!abc","9"]
    # Leading space: first char is space -> unchanged, so " abc"->" abc" [E3]
    #   and "  ab"->"  ab" [E3]. So spaces are NOT dropped/stripped.
    # Whitespace-only strings (spaces, tabs, newlines) become "" [E1,E3,E4]
    #   " "->"", "  "->"", "\t"->"", "\n"->"", "\t "->"" [E1,E3,E4]
    # Trailing whitespace is stripped: "x   "->"z" [E4]
    #   (shift first char, then strip trailing whitespace)
    # Non-breaking space \u00a0 is treated as whitespace -> "" [E4]
    #   ? Hypothesis: strip() semantics (Python str.strip) define whitespace.
    def shift(ch):
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') + 2) % 26 + ord('A'))
        return ch
    out = []
    for s in probe["inputs"]:
        if s.strip() == "":
            out.append("")  # whitespace-only -> empty [E1,E3,E4]
        else:
            out.append((shift(s[0]) + s[1:]).rstrip())
    return {"outputs": out}

def predict(probe):
    # Only the FIRST character is shifted +2 (letters, wrapping) [E1,E2,E3]
    # Rest of the string is unchanged [E1,E2,E3]
    # Non-letter first char is unchanged [E1: "1"->"1", "!"->"!", E3: "1abc","!abc","9"]
    # Leading space: first char is space -> unchanged, so " abc"->" abc" [E3]
    #   and "  ab"->"  ab" [E3]. So spaces are NOT dropped/stripped.
    # " "->"" [E1] and "  "->"" [E3]: a string of only spaces becomes empty.
    #   ? Hypothesis: if the string is all spaces, return "". Otherwise shift first char.
    #   (E1 " "->"", E3 "  "->""; but " abc"->" abc" keeps its space since not all-space.)
    def shift(ch):
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') + 2) % 26 + ord('A'))
        return ch
    out = []
    for s in probe["inputs"]:
        if s == "":
            out.append("")
        elif s.strip() == "":
            out.append("")  # all-space string -> empty [E1, E3]
        else:
            out.append(shift(s[0]) + s[1:])
    return {"outputs": out}

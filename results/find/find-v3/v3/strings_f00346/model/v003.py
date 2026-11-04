def predict(probe):
    # Rule 1: All whitespace characters (space, tab, newline, etc.) are removed [E1,E2,E5,E6]
    # Rule 2: If the first remaining character is an ASCII letter, shift it +2 in the
    #         alphabet with wrap-around (Z->B, z->b) [E1,E3,E5,E6]
    # Rule 3: If the first remaining character is not a letter (digit/symbol), no shift [E2,E4]
    # Rule 4: The shift applies to the first char AFTER whitespace removal [E2 " Abc"->"Cbc"]
    outputs = []
    for s in probe["inputs"]:
        t = ''.join(ch for ch in s if not ch.isspace())
        if t:
            c = t[0]
            if 'a' <= c <= 'z':
                c = chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
            elif 'A' <= c <= 'Z':
                c = chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
            t = c + t[1:]
        outputs.append(t)
    return {"outputs": outputs}

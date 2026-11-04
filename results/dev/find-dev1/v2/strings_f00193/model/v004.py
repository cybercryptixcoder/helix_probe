def predict(probe):
    # First char: ASCII letter -> Caesar -2 with wrap (a->y, b->z, z->x, A->Y, Z->X) [E1,E3]
    # First char: non-ASCII Unicode letter -> codepoint -2 (é->ç, Ω->Χ, 日->日, ß->Ý, µ->³, ª->¨) [E5,E6]
    # First char: non-letter -> unchanged (digits, punct, space, control, ², €, ¡, dashes, nbsp, DEL, 😀) [E1,E4,E6]
    # Rest of string: unchanged [E1-E6]
    # Append "JTQL" always [E1-E6]
    # Empty input -> "JTQL" (untested, best guess ?)
    inputs = probe.get("inputs", [])
    outputs = []
    for s in inputs:
        if not s:
            outputs.append("JTQL")
            continue
        c = s[0]
        o = ord(c)
        if 'a' <= c <= 'z':
            first = chr((o - 97 - 2) % 26 + 97)
        elif 'A' <= c <= 'Z':
            first = chr((o - 65 - 2) % 26 + 65)
        elif c.isalpha():
            first = chr(o - 2)   # ? wrap not observed for non-ASCII
        else:
            first = c
        outputs.append(first + s[1:] + "JTQL")
    return {"outputs": outputs}

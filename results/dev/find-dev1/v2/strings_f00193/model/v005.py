def predict(probe):
    # Empty input -> "HTQL" (i.e. the shift applies to an implicit char before 'J'? No: 'J'-2='H') [E8]
    # Actually: empty input -> "HTQL": treat as if first char is 'J' shifted -2 -> 'H', then "TQL" [E8]
    # First char ASCII letter -> Caesar -2 with wrap (a->y, b->z, z->x, A->Y, Z->X) [E1,E3,E7]
    # First char non-ASCII letter -> codepoint -2 (é->ç, Ω->Χ, 日->日? no: 日->日 was wrong; 日->日? E5 shows 日->日? -> 日-2=日? Actually 日 U+65E5 -> U+65E3) [E5,E6,E8]
    # First char non-letter -> unchanged (digits, punct, space, control, ², €, ¡, dashes, nbsp, DEL, 😀) [E1,E4,E6]
    # Rest of string unchanged [E1-E8]
    # Append "JTQL" always [E1-E8]
    inputs = probe.get("inputs", [])
    outputs = []
    for s in inputs:
        if not s:
            outputs.append("HTQL")
            continue
        c = s[0]
        o = ord(c)
        if 'a' <= c <= 'z':
            first = chr((o - 97 - 2) % 26 + 97)
        elif 'A' <= c <= 'Z':
            first = chr((o - 65 - 2) % 26 + 65)
        elif c.isalpha():
            first = chr(o - 2)
        else:
            first = c
        outputs.append(first + s[1:] + "JTQL")
    return {"outputs": outputs}

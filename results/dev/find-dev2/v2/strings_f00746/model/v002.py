def predict(probe):
    # Rule: strip trailing whitespace (rstrip) [E1, E3, E8]
    # Rule: shift the FIRST character of the rstripped string by +2 in the alphabet,
    #       preserving case, wrapping within a-z / A-Z [E1, E2, E4]
    # Rule: if the first character is not an ASCII letter, no shift [E3, E6, E8]
    # Rule: non-ASCII letters ARE shifted +2 too [E9]
    #   é->ë, É->Ë, ü->þ, Ü->Þ, ñ->ó, à->â, ö->ø
    #   These are Unicode codepoint +2 (é U+00E9 -> ë U+00EB, ü U+00FC -> þ U+00FE,
    #   ñ U+00F1 -> ó U+00F3, à U+00E0 -> â U+00E2, ö U+00F6 -> ø U+00F8).
    #   So: if first char is a letter (Unicode), shift by +2 codepoints.
    #   For ASCII letters, codepoint+2 also works within a-z/A-Z except wrap at y/z.
    #   Wrap: y->a, z->b, Y->A, Z->B [E4]. For non-ASCII, no wrap evidence; use +2.
    s = probe.get("inputs", [])
    out = []
    for x in s:
        if not isinstance(x, str):
            out.append(x)
            continue
        y = x.rstrip()
        if y and y[0].isalpha():
            c = y[0]
            if 'a' <= c <= 'z':
                c2 = chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
            elif 'A' <= c <= 'Z':
                c2 = chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
            else:
                # non-ASCII letter: shift by +2 codepoints (no wrap evidence) [E9]
                c2 = chr(ord(c) + 2)
            y = c2 + y[1:]
        out.append(y)
    return {"outputs": out}

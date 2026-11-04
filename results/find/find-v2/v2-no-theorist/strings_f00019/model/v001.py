def predict(probe):
    # Observations [E1]:
    #  "abc123" -> "abc123" (unchanged)
    #  "level" -> "levem" (last char l->m)
    #  " Zebralower" -> " Zebralowes" (last char r->s)
    #  "Hello World function lazy" -> "...lazz" (last char y->z)
    #  "bananaUPPER" -> "bananaUPPES" (last char R->S)
    #  "Zebra" -> "Zebrb" (last char a->b)
    # Rule: last character is shifted forward by 1 in the alphabet.
    #  - letters a-z / A-Z: next letter (wrapping? unknown, assume wrap z->a)
    #  - digits/symbols: unchanged? "abc123" ends in '3' and stayed '3'.
    #    So only alphabetic last chars are shifted; non-alpha unchanged.
    # "?" wrap-around for z/Z is a guess.
    def shift(ch):
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') + 1) % 26 + ord('a'))
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') + 1) % 26 + ord('A'))
        return ch

    out = []
    for s in probe.get("inputs", []):
        if s:
            s = s[:-1] + shift(s[-1])
        out.append(s)
    return {"outputs": out}

def predict(probe):
    # Hypothesis: for each input, the first character is shifted by -1 in the
    # alphabet if it is a lowercase letter (a->z? no: a->y, l->j, b->z, h->f, z->x).
    # Observed first-char changes: a->y, l->j, b->z, H->F, b->z, Z->X.
    # That's a shift of -2 in the alphabet (wrapping), preserving case.
    # Leading space input " Zebralower" was unchanged -> only shift if first char is a letter.
    # Rest of the string unchanged.
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
        return c
    outs = []
    for s in probe["inputs"]:
        if s and s[0].isalpha():
            outs.append(shift(s[0]) + s[1:])
        else:
            outs.append(s)
    return {"outputs": outs}

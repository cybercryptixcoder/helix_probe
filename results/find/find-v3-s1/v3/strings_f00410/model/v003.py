def predict(probe):
    # The box reverses the input string [E1-E6: every output is the reverse].
    # Then it shifts the FIRST character of the reversed string back by 2
    # positions in the alphabet, preserving case [E4: cat->tac->rac; E6: aZ->Za->Xa].
    # Non-letter first characters are left unchanged [E2: "123 456"->"654 321"; E3: "level123"->"321level"].
    out = []
    for s in probe["inputs"]:
        r = s[::-1]
        if r:
            c = r[0]
            if 'a' <= c <= 'z':
                c = chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
            elif 'A' <= c <= 'Z':
                c = chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
            r = c + r[1:]
        out.append(r)
    return {"outputs": out}

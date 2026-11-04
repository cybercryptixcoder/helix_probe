def predict(probe):
    # Rule: delete every uppercase 'R', then increment the last character.
    #   - Uppercase 'R' is removed wherever it appears [E4: RAIN->AIO, WORD->WOE,
    #     bananaUPPER->bananaUPPF]
    #   - Lowercase 'r' is NOT removed [E1: Zebralower->Zebralowes]
    #   - Last char: a-z +1 (z->a), A-Z +1 (Z->A), digits/others unchanged
    #     [E1,E2,E3,E4]
    #   - Increment happens AFTER removal, on the new last char [E4: RAIN->AIO]
    def inc(c):
        if 'a' <= c <= 'z':
            return 'a' if c == 'z' else chr(ord(c)+1)
        if 'A' <= c <= 'Z':
            return 'A' if c == 'Z' else chr(ord(c)+1)
        return c
    def transform(s):
        s = s.replace('R', '')
        if not s:
            return s
        return s[:-1] + inc(s[-1])
    return {"outputs": [transform(x) for x in probe["inputs"]]}

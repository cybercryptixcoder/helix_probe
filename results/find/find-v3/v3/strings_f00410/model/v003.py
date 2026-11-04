def predict(probe):
    # Reverse whole string [E1, E2]
    # Then shift the FIRST character of the reversed string back by 2,
    #   but ONLY if it is a letter (a-z / A-Z). Digits and spaces unchanged [E4].
    #   "01"->"10" (first char '1' digit, unchanged), "0"->"0", "9"->"9",
    #   "10"->"01", "abc0"->"0cba" (first char '0' digit unchanged),
    #   "a0"->"0a" (first char '0' unchanged). Letters: "Zz"->"xZ" (Z->x),
    #   "zZ"->"Xz" (z->X). [E1, E4]
    # Letter shift wraps within alphabet, preserving case [E1: a->y, R->P].
    def f(s):
        r = s[::-1]
        if r and r[0].isalpha():
            c = r[0]
            if c.islower():
                c = chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
            else:
                c = chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
            r = c + r[1:]
        return r
    return {"outputs": [f(s) for s in probe["inputs"]]}

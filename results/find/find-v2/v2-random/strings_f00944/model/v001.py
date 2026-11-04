def predict(probe):
    # Last character of each input is shifted +1 in alphabet (wraps z->a) [E1]
    #   "level"->"levem" (l->m), "Zebra"->"Zebrb" (a->b), "bananaUPPER"->"bananaUPPF" (R->S)
    #   "lazy"->"lazz" (y->z), "Zebralower"->"Zebralowes" (r->s)
    # Non-letter last chars unchanged: "abc123"->"abc123" (3 stays 3) [E1]
    # Case preserved: uppercase letter shifts within uppercase [E1]
    # Only the final character changes; rest of string untouched [E1]
    def shift(s):
        if not s:
            return s
        c = s[-1]
        if 'a' <= c <= 'z':
            n = chr((ord(c) - ord('a') + 1) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            n = chr((ord(c) - ord('A') + 1) % 26 + ord('A'))
        else:
            n = c
        return s[:-1] + n
    return {"outputs": [shift(x) for x in probe["inputs"]]}

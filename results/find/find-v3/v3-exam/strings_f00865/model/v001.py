def predict(probe):
    # Rule: the first character of each input is shifted one step backward
    #   in the alphabet, case preserved; everything else unchanged.
    # Evidence E1: "abc123"->"ybc123" (a->y, wrap), "level"->"jevel" (l->j),
    #   "Hello..."->"Fello..." (H->F), "bananaUPPER"->"zananaUPPER" (b->z),
    #   "Zebra"->"Xebra" (Z->X). " Zebralower" starts with space -> unchanged.
    def shift(s):
        if not s:
            return s
        c = s[0]
        if 'a' <= c <= 'z':
            c = chr((ord(c) - ord('a') - 1) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            c = chr((ord(c) - ord('A') - 1) % 26 + ord('A'))
        return c + s[1:]
    return {"outputs": [shift(s) for s in probe["inputs"]]}

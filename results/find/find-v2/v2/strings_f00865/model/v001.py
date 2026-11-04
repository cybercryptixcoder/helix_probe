def predict(probe):
    # First letter: a->y, b->z, H->F, l->j, Z->X [E1]
    #   i.e. first char shifted by -2 in alphabet (case preserved)
    # Other letters unchanged [E1: "abc123"->"ybc123", "level"->"jevel",
    #   "Hello World..."->"Fello World...", "bananaUPPER"->"zananaUPPER",
    #   "Zebra"->"Xebra"]
    # Leading space input unchanged [E1: " Zebralower"->" Zebralower"]
    #   (first char is space, not a letter, so no shift)
    # Digits/symbols in first position: ? assume unchanged
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
        return c
    out = []
    for s in probe["inputs"]:
        if s:
            out.append(shift(s[0]) + s[1:])
        else:
            out.append(s)
    return {"outputs": out}

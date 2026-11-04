def predict(probe):
    # Split on whitespace, reverse each word, double first char of the LAST
    # reversed word only, rejoin with single spaces [E2, E3].
    #   "ab cd" -> "ba ddc" [E2]; "test case" -> "tset eesac" [E3]
    #   "a b c" -> "a b cc" [E2]; single word always doubled [E1,E2]
    def g(w):
        return w[::-1]
    out = []
    for s in probe["inputs"]:
        ws = s.split()
        if not ws:
            out.append("")
            continue
        r = [g(w) for w in ws]
        r[-1] = r[-1][0] + r[-1]
        out.append(" ".join(r))
    return {"outputs": out}

def predict(probe):
    # Observations from E1:
    # "apple" -> "cpple": first letter a->c (+2), rest unchanged
    # "test case " -> "vestcase": t->v (+2), space removed
    # "test caseMiXeD" -> "vestcaseMiXeD": t->v, space removed
    # "data a Python " -> "fataaPython": d->f (+2), spaces removed
    # "test case Zebra" -> "vestcaseZebra": t->v, space removed
    # "Mississippi Hello World data" -> "OississippiHelloWorlddata": M->O (+2), spaces removed
    # Rule: shift first char +2 in alphabet, remove all spaces.
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
        return c
    outs = []
    for s in probe["inputs"]:
        s2 = s.replace(" ", "")
        if s2:
            s2 = shift(s2[0]) + s2[1:]
        outs.append(s2)
    return {"outputs": outs}

def predict(probe):
    # First alphabetic char of each word is shifted +1 in the alphabet [E1]
    # Other chars unchanged; spaces removed [E1]
    # "abc123"->"cbc123": a->c, b,c unchanged? Actually a->c is +2? Check: a->c (+2)
    # "level"->"nevel": l->n (+2), rest same
    # " Zebralower"->"Bebralower": Z->B (+2), space removed
    # "Hello World function lazy"->"JelloWorldfunctionlazy": H->J (+2), spaces removed
    # "bananaUPPER"->"dananaUPPER": b->d (+2)
    # "Zebra"->"Bebra": Z->B (+2)
    # So: first letter of each word shifted +2, spaces removed, rest unchanged
    import re
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c)-ord('a')+2)%26+ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c)-ord('A')+2)%26+ord('A'))
        return c
    out = []
    for s in probe["inputs"]:
        words = s.split()
        res = []
        for w in words:
            if w and w[0].isalpha():
                res.append(shift(w[0]) + w[1:])
            else:
                res.append(w)
        out.append("".join(res))
    return {"outputs": out}

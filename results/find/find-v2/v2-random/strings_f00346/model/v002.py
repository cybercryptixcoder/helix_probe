def predict(probe):
    # First alphabetic char of each word shifted +2 in alphabet [E1, E2]
    # Spaces removed [E1, E2]
    # Other chars unchanged [E1, E2]
    # "test case"->"vestcase": t->v (+2), but "case"->"case" unchanged? 
    #   Actually "test case"->"vestcase": t->v (+2), then "est" unchanged, "case" unchanged
    #   Wait: only FIRST char of the whole string? "test case"->"vestcase" (t->v, rest same)
    # "banana data banana"->"dananadatabanana": b->d (+2), rest unchanged (only first char!)
    # "Hello World function lazy"->"JelloWorldfunctionlazy": H->J (+2), rest unchanged
    # " Zebralower"->"Bebralower": Z->B (+2), rest unchanged
    # So: only the FIRST alphabetic char of the ENTIRE string is shifted +2, spaces removed
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c)-ord('a')+2)%26+ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c)-ord('A')+2)%26+ord('A'))
        return c
    out = []
    for s in probe["inputs"]:
        t = s.replace(" ", "")
        res = []
        done = False
        for c in t:
            if not done and c.isalpha():
                res.append(shift(c))
                done = True
            else:
                res.append(c)
        out.append("".join(res))
    return {"outputs": out}

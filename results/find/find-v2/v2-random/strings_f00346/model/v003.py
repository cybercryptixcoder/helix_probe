def predict(probe):
    # Rules (evidence):
    # 1. All whitespace (spaces AND tabs) is removed [E9: "worldtab\tsep"->"yorldtabsep"]
    # 2. Only the FIRST alphabetic char of the ENTIRE string is shifted +2 in alphabet [E1-E9]
    # 3. Case preserved; non-alpha chars unchanged [E1-E9]
    # 4. Shift wraps within same case (Z->B, z->b) [E1, E8]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c)-ord('a')+2)%26+ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c)-ord('A')+2)%26+ord('A'))
        return c
    out = []
    for s in probe["inputs"]:
        t = "".join(ch for ch in s if not ch.isspace())
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

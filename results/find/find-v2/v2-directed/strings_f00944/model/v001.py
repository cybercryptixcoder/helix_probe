def predict(probe):
    # Last alphabetic char of each word shifts +1 in alphabet, preserving case [E1]
    # Non-alphabetic chars unchanged [E1: "12345","a1b2c3","hello!","  spaced  "]
    # Only the final letter of each whitespace-separated word changes [E1]
    # "hello"->"hellp", "world"->"worle", "fox"->"foy" [E1]
    # Wrap? unknown; assume simple +1 with z->a? [E1 no z case]
    def shift_word(w):
        # find last alphabetic character
        idx = -1
        for i, c in enumerate(w):
            if c.isalpha():
                idx = i
        if idx == -1:
            return w
        c = w[idx]
        if c == 'z':
            nc = 'a'
        elif c == 'Z':
            nc = 'A'
        else:
            nc = chr(ord(c) + 1)
        return w[:idx] + nc + w[idx+1:]

    def transform(s):
        # split preserving whitespace
        out = []
        i = 0
        n = len(s)
        while i < n:
            if s[i].isspace():
                out.append(s[i])
                i += 1
            else:
                j = i
                while j < n and not s[j].isspace():
                    j += 1
                out.append(shift_word(s[i:j]))
                i = j
        return ''.join(out)

    return {"outputs": [transform(x) for x in probe["inputs"]]}

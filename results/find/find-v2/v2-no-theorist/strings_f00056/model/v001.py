def predict(probe):
    # Rule 1: remove duplicate chars, keep first occurrence, case-sensitive, across whole string [E1]
    # Rule 2: shift first char down 1 in alphabet (a->z, A->Z wrap); non-letters unchanged [E1]
    def f(s):
        seen = set()
        out = []
        for ch in s:
            if ch not in seen:
                seen.add(ch)
                out.append(ch)
        res = ''.join(out)
        if res:
            c = res[0]
            if 'a' <= c <= 'z':
                res = chr((ord(c) - ord('a') - 1) % 26 + ord('a')) + res[1:]
            elif 'A' <= c <= 'Z':
                res = chr((ord(c) - ord('A') - 1) % 26 + ord('A')) + res[1:]
        return res
    return {"outputs": [f(x) for x in probe["inputs"]]}

def predict(probe):
    # Last char incremented to next letter; non-letters (space) unchanged [E1]
    # 'z' wraps to 'a' (not to '{') [E2]
    out = []
    for s in probe["inputs"]:
        if s and s[-1].isalpha():
            c = s[-1]
            if c == 'z':
                out.append(s[:-1] + 'a')
            elif c == 'Z':
                out.append(s[:-1] + 'A')
            else:
                out.append(s[:-1] + chr(ord(c) + 1))
        else:
            out.append(s)
    return {"outputs": out}

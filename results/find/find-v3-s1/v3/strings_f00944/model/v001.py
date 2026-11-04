def predict(probe):
    # Last char incremented to next letter; non-letters (space) unchanged [E1]
    out = []
    for s in probe["inputs"]:
        if s and s[-1].isalpha():
            out.append(s[:-1] + chr(ord(s[-1]) + 1))
        else:
            out.append(s)
    return {"outputs": out}

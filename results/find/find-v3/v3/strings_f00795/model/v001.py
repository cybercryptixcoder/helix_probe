def predict(probe):
    # Insert "2" at index len//2 [E1]
    # Shift last char +2 in alphabet if letter, preserve case, wrap [E1]
    # Digits/symbols last char unchanged [E1: abc123]
    out = []
    for s in probe["inputs"]:
        pos = len(s) // 2
        t = s[:pos] + "2" + s[pos:]
        if t:
            c = t[-1]
            if 'a' <= c <= 'z':
                t = t[:-1] + chr((ord(c)-ord('a')+2) % 26 + ord('a'))
            elif 'A' <= c <= 'Z':
                t = t[:-1] + chr((ord(c)-ord('A')+2) % 26 + ord('A'))
        out.append(t)
    return {"outputs": out}

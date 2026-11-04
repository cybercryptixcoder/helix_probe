def predict(probe):
    # Insert "2" at index len//2 [E1]
    # Shift last char +2 within its case if letter (wrap), else unchanged [E1]
    out = []
    for s in probe["inputs"]:
        mid = len(s) // 2
        t = s[:mid] + "2" + s[mid:]
        if t:
            c = t[-1]
            if 'a' <= c <= 'z':
                c = chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
            elif 'A' <= c <= 'Z':
                c = chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
            t = t[:-1] + c
        out.append(t)
    return {"outputs": out}

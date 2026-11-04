def predict(probe):
    # Insert '4' at index len//2 [E1: all 6 cases match len//2]
    # If last char is a letter, increment it by 1 in ASCII [E1: l→m,r→s,y→z,R→S,a→b]
    # Digits/other last chars unchanged [E1: abc123 ends '3'→'3']
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append(s)
            continue
        i = len(s) // 2
        t = s[:i] + "4" + s[i:]
        if t[-1].isalpha():
            t = t[:-1] + chr(ord(t[-1]) + 1)
        out.append(t)
    return {"outputs": out}

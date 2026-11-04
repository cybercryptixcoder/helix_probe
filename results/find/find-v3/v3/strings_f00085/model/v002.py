def predict(probe):
    # Insert '4' at index len//2 [E1-E4]
    # If last char is a letter, increment it by 1 in ASCII [E1-E4]
    # Digits/other last chars unchanged [E1: abc123 ends '3'→'3']
    # Increment applies to original last char, before insertion [E4: az→a4a, zz→z4a]
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append(s)
            continue
        if s[-1].isalpha():
            s = s[:-1] + chr(ord(s[-1]) + 1)
        i = len(s) // 2
        out.append(s[:i] + "4" + s[i:])
    return {"outputs": out}

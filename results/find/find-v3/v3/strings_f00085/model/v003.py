def predict(probe):
    # Insert '4' at index len//2 [E1-E4]
    # If last char is a letter, increment it by 1 in ASCII, wrapping z->a and Z->A [E1-E4, E8]
    # Digits/other last chars unchanged [E1: abc123 ends '3'→'3']
    # Increment applies to original last char, before insertion [E4: az→a4a, zz→z4a]
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append(s)
            continue
        if s[-1].isalpha():
            c = s[-1]
            if c == 'z':
                c = 'a'
            elif c == 'Z':
                c = 'A'
            else:
                c = chr(ord(c) + 1)
            s = s[:-1] + c
        i = len(s) // 2
        out.append(s[:i] + "4" + s[i:])
    return {"outputs": out}

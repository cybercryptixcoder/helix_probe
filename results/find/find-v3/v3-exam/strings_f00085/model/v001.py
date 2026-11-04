def predict(probe):
    # Insert "4" at index len(s)//2 [E1: all 6 cases]
    # Shift last char up by 1 in alphabet [E1: l->m, r->s, y->z, R->S, a->b]
    # Wrap z->a, Z->A? [E1, unconfirmed]
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append(s)
            continue
        mid = len(s) // 2
        t = s[:mid] + "4" + s[mid:]
        last = t[-1]
        if 'a' <= last <= 'z':
            last = chr((ord(last) - ord('a') + 1) % 26 + ord('a'))
        elif 'A' <= last <= 'Z':
            last = chr((ord(last) - ord('A') + 1) % 26 + ord('A'))
        out.append(t[:-1] + last)
    return {"outputs": out}

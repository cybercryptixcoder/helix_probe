def predict(probe):
    # Insert '4' before char at index len//2 [E1: hello,abc,123,a b c,Test!,spaced,world]
    # Last char: if letter, shift +1 preserving case, wrap z->a (?) [E1: o->p,d->e,c->d,O->P]
    # Non-letter last char unchanged [E1: "123","Test!","  spaced  "]
    out = []
    for s in probe["inputs"]:
        n = len(s)
        mid = n // 2
        r = s[:mid] + "4" + s[mid:]
        if r:
            c = r[-1]
            if 'a' <= c <= 'z':
                r = r[:-1] + chr((ord(c) - ord('a') + 1) % 26 + ord('a'))
            elif 'A' <= c <= 'Z':
                r = r[:-1] + chr((ord(c) - ord('A') + 1) % 26 + ord('A'))
        out.append(r)
    return {"outputs": out}

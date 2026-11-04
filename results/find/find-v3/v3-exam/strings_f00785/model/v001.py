def predict(probe):
    # First char: if letter, +1 with wrap (Z->A, z->a); else unchanged [E1]
    # Append 'y' if string doesn't already end with 'y' [E1]
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append(s)
            continue
        c = s[0]
        if 'a' <= c <= 'z':
            c = 'a' if c == 'z' else chr(ord(c)+1)
        elif 'A' <= c <= 'Z':
            c = 'A' if c == 'Z' else chr(ord(c)+1)
        r = c + s[1:]
        if not r.endswith('y'):
            r += 'y'
        out.append(r)
    return {"outputs": out}

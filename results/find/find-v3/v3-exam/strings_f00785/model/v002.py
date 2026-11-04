def predict(probe):
    # First char: if letter, +1 with wrap (Z->A, z->a); else unchanged [E1-E6]
    # Append 'y' unless the ORIGINAL string already ends with 'y' [E4, E6]
    #   (E6: "y"->"z" no append; "ay"->"by" no append; "zy"->"ay" no append)
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
        if not s.endswith('y'):
            r += 'y'
        out.append(r)
    return {"outputs": out}

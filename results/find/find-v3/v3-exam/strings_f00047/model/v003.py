def predict(probe):
    # Lowercase whole string, then uppercase first char [E1, E2]
    # Trailing whitespace is stripped [E3]
    # Leading spaces preserved; first char uppercased only if letter [E2, E6]
    # Uppercase uses per-character mapping: ß -> Ss (not SS) [E6]
    out = []
    for s in probe["inputs"]:
        t = s.lower().rstrip()
        if t:
            c = t[0]
            u = c.upper()
            # Python's str.upper on 'ß' gives 'SS'; box gives 'Ss'
            if c == '\u00df':
                u = 'Ss'
            t = u + t[1:]
        out.append(t)
    return {"outputs": out}

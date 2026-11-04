def predict(probe):
    # Lowercase whole string, then uppercase first char [E1, E2]
    # Trailing whitespace is stripped [E3: "banana data banana " -> "Banana data banana"]
    # Leading spaces preserved, first char uppercased only if letter [E2]
    out = []
    for s in probe["inputs"]:
        t = s.lower().rstrip()
        if t:
            t = t[0].upper() + t[1:]
        out.append(t)
    return {"outputs": out}

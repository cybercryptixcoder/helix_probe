def predict(probe):
    # Lowercase everything, then capitalize the very first character if alphabetic [E1, E2, E3]
    # If first char is not alphabetic, nothing is capitalized [E2]
    # Trailing whitespace is stripped [E3: "banana data banana " -> "Banana data banana"]
    # Leading spaces preserved, no capitalization of later words [E1, E2]
    out = []
    for s in probe["inputs"]:
        t = s.lower().rstrip()
        if t and t[0].isalpha():
            t = t[0].upper() + t[1:]
        out.append(t)
    return {"outputs": out}

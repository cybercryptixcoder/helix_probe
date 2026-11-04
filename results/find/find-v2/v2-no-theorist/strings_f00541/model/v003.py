def predict(probe):
    # Leading 'H' or ' ' are stripped repeatedly [E1, E2]
    # Trailing whitespace is also stripped [E3: "banana data banana " -> "banana data banana"]
    # Interior characters untouched [E1, E2, E3]
    out = []
    for s in probe["inputs"]:
        i = 0
        while i < len(s) and s[i] in ("H", " "):
            i += 1
        out.append(s[i:].rstrip())
    return {"outputs": out}

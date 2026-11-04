def predict(probe):
    # Rule: t = s.capitalize() — first char upper, all others lower [E1 all 6]
    # Rule: insert "10" at index len(t)//2 [E1 all 6]
    out = []
    for s in probe["inputs"]:
        t = s.capitalize()
        i = len(t) // 2
        out.append(t[:i] + "10" + t[i:])
    return {"outputs": out}

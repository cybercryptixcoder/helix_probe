def predict(probe):
    # Rule: t = s.capitalize() — first char upper, all others lower [E1..E11]
    # Rule: insert "10" at index len(t)//2 [E1..E11]
    # Rule: but if t is a single character, capitalize is skipped (stays as-is) [E11: "a" -> "10a"]
    out = []
    for s in probe["inputs"]:
        t = s.capitalize() if len(s) > 1 else s
        i = len(t) // 2
        out.append(t[:i] + "10" + t[i:])
    return {"outputs": out}

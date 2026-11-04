def predict(probe):
    # Removes all whitespace (spaces, tabs, newlines, unicode whitespace) [E1,E2,E6,E7,E8,E9]
    # Appends "F" only if the result does not already end with "F" [E10]
    # Case, digits, symbols preserved [E1,E4]
    import re
    out = []
    for s in probe["inputs"]:
        t = re.sub(r"\s", "", s)
        if not t.endswith("F"):
            t += "F"
        out.append(t)
    return {"outputs": out}

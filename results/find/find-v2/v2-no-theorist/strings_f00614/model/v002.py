def predict(probe):
    # Removes all whitespace (spaces, tabs, newlines) [E1, E2]
    # Appends "F" only if result doesn't already end in "F" [E2: "F"->"F", "alreadyF"->"alreadyF"]
    # Empty input -> "F" [E2]
    import re
    out = []
    for x in probe["inputs"]:
        s = re.sub(r"\s", "", x)
        if not s.endswith("F"):
            s += "F"
        out.append(s)
    return {"outputs": out}

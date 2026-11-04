def predict(probe):
    # Removes all whitespace (spaces, tabs, newlines) [E1, E2]
    # Appends 'F' only if the result doesn't already end with 'F' [E2: "F" -> "F", "aFb" -> "aFbF"]
    # Case, digits, punctuation preserved [E1, E2]
    import re
    out = []
    for s in probe["inputs"]:
        t = re.sub(r"\s", "", s)
        if not t.endswith("F"):
            t = t + "F"
        out.append(t)
    return {"outputs": out}

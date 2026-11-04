def predict(probe):
    # Split on any whitespace (spaces, tabs, newlines) [E4]
    # Drop empty words [E2]
    # Reverse each word [E1, E2]
    # Prefix "lmKA" to last word; if input ends with whitespace (or empty), append standalone "lmKA" [E2, E4]
    import re
    out = []
    for s in probe.get("inputs", []):
        words = s.split()
        rev = [w[::-1] for w in words]
        if not words or (s and s[-1].isspace()):
            rev.append("lmKA")
        else:
            rev[-1] = "lmKA" + rev[-1]
        out.append(" ".join(rev))
    return {"outputs": out}

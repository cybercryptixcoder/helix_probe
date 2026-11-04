def predict(probe):
    # Split on spaces, drop empty words, reverse each word [E1, E2]
    # Prefix "lmKA" to last word; if input ends with space (or is empty), append standalone "lmKA" instead [E2]
    out = []
    for s in probe.get("inputs", []):
        words = [w for w in s.split(" ") if w]
        rev = [w[::-1] for w in words]
        if s.endswith(" ") or not words:
            rev.append("lmKA")
        else:
            rev[-1] = "lmKA" + rev[-1]
        out.append(" ".join(rev))
    return {"outputs": out}

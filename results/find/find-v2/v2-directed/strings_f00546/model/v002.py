def predict(probe):
    # Split on whitespace (no arg) -> collapses runs, drops leading/trailing [E1,E2]
    # Reverse each word [E1,E2]
    # Prefix "lmKA" to the LAST word [E1,E2]
    # Join with single spaces [E1,E2]
    out = []
    for x in probe.get("inputs", []):
        w = x.split()
        if w:
            w = [s[::-1] for s in w]
            w[-1] = "lmKA" + w[-1]
            out.append(" ".join(w))
        else:
            out.append("lmKA")
    return {"outputs": out}

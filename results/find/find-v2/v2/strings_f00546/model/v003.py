def predict(probe):
    # Split on whitespace, collapse runs, strip [E2]
    # Reverse each word, join with single spaces [E1, E2]
    # If input has trailing whitespace: append " lmKA" at end [E2, E3]
    # Else: insert "lmKA" immediately before last word [E1, E2]
    # Empty/whitespace-only -> "lmKA" [E2]
    try:
        out = []
        for x in probe["inputs"]:
            words = x.split()
            if not words:
                out.append("lmKA")
                continue
            rev = [w[::-1] for w in words]
            if x != x.rstrip():
                out.append(" ".join(rev) + " lmKA")
            else:
                rev[-1] = "lmKA" + rev[-1]
                out.append(" ".join(rev))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}

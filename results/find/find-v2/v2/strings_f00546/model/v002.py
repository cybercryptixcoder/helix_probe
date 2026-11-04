def predict(probe):
    # Rule: split input on any whitespace (spaces, tabs, newlines), collapsing runs [E2]
    # Rule: strip leading/trailing whitespace; empty result -> "lmKA" [E2]
    # Rule: reverse each word, join with single spaces [E1, E2]
    # Rule: insert "lmKA" immediately before the last word [E1, E2]
    #   single word -> "lmKA" + reversed word [E1]
    #   empty -> "lmKA" [E2]
    try:
        out = []
        for x in probe["inputs"]:
            words = x.split()
            if not words:
                out.append("lmKA")
                continue
            rev = [w[::-1] for w in words]
            rev[-1] = "lmKA" + rev[-1]
            out.append(" ".join(rev))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}

def predict(probe):
    # Split on runs of spaces; empty words are dropped (collapsed) [E2, E4]
    # Leading/trailing spaces produce no empty words [E2, E4]
    # Reverse each word's letters [E1, E2]
    # Single word: "lmKA" + reversed word [E1]
    # Multi-word: reversed words joined by space, then " lmKA" + last reversed word [E1]
    # Empty input / all spaces: "lmKA" [E2, E4]
    out = []
    for s in probe["inputs"]:
        words = [w for w in s.split(" ") if w != ""]
        rev = [w[::-1] for w in words]
        if len(rev) == 0:
            out.append("lmKA")
        elif len(rev) == 1:
            out.append("lmKA" + rev[0])
        else:
            out.append(" ".join(rev[:-1]) + " lmKA" + rev[-1])
    return {"outputs": out}

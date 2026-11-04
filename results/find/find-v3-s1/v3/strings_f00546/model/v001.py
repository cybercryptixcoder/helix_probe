def predict(probe):
    # Split input on spaces; reverse each word; insert literal "lmKA" before the last word [E1]
    # Single word: "lmKA" + reversed word [E1 "apple" -> "lmKAelppa"]
    # Multi-word: reversed words joined by space, then " lmKA" + last reversed word [E1 all cases]
    # Trailing space yields an empty last word, so "lmKA" lands at the end [E1 "test case ", "data a Python "]
    out = []
    for s in probe["inputs"]:
        words = s.split(" ")
        rev = [w[::-1] for w in words]
        if len(rev) == 1:
            out.append("lmKA" + rev[0])
        else:
            out.append(" ".join(rev[:-1]) + " lmKA" + rev[-1])
    return {"outputs": out}

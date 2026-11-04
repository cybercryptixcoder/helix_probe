def predict(probe):
    # Rules (from evidence):
    # - Split input into whitespace-separated tokens [E2: "one  two", "a\tb", "  lead", "trail  "]
    # - Reverse each token in place, keep token order [E1, E2]
    # - Join tokens with a single space (whitespace runs collapse) [E2: "one  two"->"eno owt", "one   two   three"->"eno owt eerht"]
    # - Prefix "lmKA" to the last token [E1, E2]
    # - Leading/trailing whitespace stripped [E1 " Zebralower", E2 "  lead", "trail  "]
    # - Empty input -> "lmKA" [guess ?]
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

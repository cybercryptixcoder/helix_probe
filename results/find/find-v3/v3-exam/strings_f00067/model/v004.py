def predict(probe):
    # Reverse each whitespace-separated word [E1,E2,E3]
    # Rejoin with single spaces [E2,E4]
    # Double first char of LAST reversed word, UNLESS the input ends with
    #   whitespace, in which case no doubling [E4]:
    #     "aa bb"->"aa bbb", "aa bb "->"aa bb", "  aa bb  "->"aa bb",
    #     " aa bb"->"aa bbb" [E4]
    # Empty/whitespace-only -> "" [E2]
    out = []
    for s in probe["inputs"]:
        ws = s.split()
        if not ws:
            out.append("")
            continue
        r = [w[::-1] for w in ws]
        if not s[-1:].isspace():
            r[-1] = r[-1][0] + r[-1]
        out.append(" ".join(r))
    return {"outputs": out}

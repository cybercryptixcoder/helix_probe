def predict(probe):
    # Reverse each whitespace-separated token, join with single space [E1-E7]
    # Internal whitespace runs collapse to one space; ends stripped [E1-E5]
    # Empty/whitespace-only -> "" [E1,E3]
    # Then append "I" only if the result doesn't already end with "I" [E8]
    #   - "a b I" -> tokens "a","b","I" -> "a b I" already ends I -> unchanged [E8]
    #   - "I" -> "I" -> unchanged [E8]
    #   - "I I" -> "I I" -> unchanged [E8]
    #   - "1 I" -> "1 I" -> unchanged [E8]
    #   - "! I" -> "! I" -> unchanged [E8]
    #   - "aI" -> "Ia" -> append -> "IaI" [E8]
    #   - "a I b" -> "a I b" -> append -> "a I bI" [E8]
    out = []
    for s in probe.get("inputs", []):
        toks = s.split()
        r = " ".join(t[::-1] for t in toks)
        if not r.endswith("I"):
            r += "I"
        out.append(r)
    return {"outputs": out}

def predict(probe):
    # Rule: strip a single leading space if present [E1: " Zebralower"->"Zebralower"]
    # Rule: if string starts with "H", drop the leading "H" [E1: "Hello World..."->"ello World..."]
    #   (only evidence is that one case; "H" removal vs "Hello" removal ambiguous)
    # Rule: otherwise return unchanged [E1: abc123, level, bananaUPPER, Zebra unchanged]
    # "?" uncertain: whether it's "strip leading H" or "strip leading 'He'"/"Hello"
    out = []
    for s in probe["inputs"]:
        if s.startswith(" "):
            s = s[1:]
        elif s.startswith("H"):
            s = s[1:]
        out.append(s)
    return {"outputs": out}

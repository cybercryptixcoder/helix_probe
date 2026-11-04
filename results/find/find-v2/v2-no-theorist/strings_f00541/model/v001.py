def predict(probe):
    # Hypothesis: f removes a leading space if present [E1: " Zebralower" -> "Zebralower"]
    # Hypothesis: f removes a leading "H" if present [E1: "Hello World..." -> "ello World..."]
    # All other inputs pass through unchanged [E1: abc123, level, bananaUPPER, Zebra unchanged]
    # "?" - unclear whether it's "strip leading whitespace" or "remove leading H"; both fit E1.
    # "?" - could be "remove first char if it's uppercase H or a space". Best guess below.
    out = []
    for s in probe["inputs"]:
        if s.startswith(" "):
            s = s[1:]
        elif s.startswith("H"):
            s = s[1:]
        out.append(s)
    return {"outputs": out}

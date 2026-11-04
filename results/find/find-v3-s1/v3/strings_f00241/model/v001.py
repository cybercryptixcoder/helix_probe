def predict(probe):
    # Only evidence: E1. "test caseMiXeD" -> "test caseMiXeJ": final D became J.
    # Everything else passed through unchanged (apple, trailing-space strings,
    # "data a Python ", "test case Zebra", "Mississippi Hello World data").
    # Hypothesis (?): the box uppercases the last character, then maps D->J?
    # That's too speculative. Simpler: only a trailing 'D' at end of string
    # becomes 'J'? But "data a Python " ends in space, unchanged; "test case "
    # ends in space, unchanged. No other string ends in 'D'.
    # Best guess (?): replace a final 'D' with 'J'; otherwise identity.
    out = []
    for s in probe["inputs"]:
        if s.endswith("D"):
            s = s[:-1] + "J"
        out.append(s)
    return {"outputs": out}

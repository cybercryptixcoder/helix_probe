def predict(probe):
    # Identity for most inputs [E1, E2]
    # Last character 'D' -> 'J' when input is mixed case? [E3: "aMiXeD" -> "aMiXeJ"]
    #   Only observed change: trailing 'D' became 'J'. Unclear if case-dependent.
    #   Hypothesis (?): a trailing 'D' is replaced by 'J'.
    out = []
    for s in probe["inputs"]:
        if s.endswith("D"):
            s = s[:-1] + "J"
        out.append(s)
    return {"outputs": out}

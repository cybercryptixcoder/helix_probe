def predict(probe):
    # Rule: uppercase the first character of the string, lowercase the rest [E1,E2,E3]
    # Rule: trailing whitespace is stripped from the result [E3: "banana data banana " -> "Banana data banana"]
    # Rule: leading whitespace is preserved (first char is space, unchanged) [E2: "  two  spaces" -> "  two  spaces"]
    # Rule: internal whitespace preserved [E2]
    # Rule: digits/symbols unaffected by case; only first char uppercased if it's a letter [E2: "123abc"->"123abc", "abc123"->"Abc123"]
    outs = []
    for s in probe["inputs"]:
        if not s:
            outs.append(s)
        else:
            t = s[0].upper() + s[1:].lower()
            outs.append(t.rstrip())
    return {"outputs": outs}

def predict(probe):
    # Rule: remove all whitespace characters (spaces, tabs, newlines) [E2, E4, E6]
    # Rule: capitalize first char of the whole string, lowercase the rest [E1, E2, E4, E5, E6]
    # Rule: leading whitespace is removed before capitalization, so a string
    #       starting with whitespace is NOT capitalized [E4 "  hello"->"hello", E6 "  tab\there"->"tabhere"]
    # Rule: non-whitespace separators (., /, -, _, digits) do NOT trigger capitalization [E4, E6]
    import re
    out = []
    for s in probe["inputs"]:
        # remove all whitespace chars
        s = re.sub(r"\s", "", s)
        # capitalize only if the original had no leading whitespace
        # (after removing whitespace we can't tell; so check original)
        out.append(s)
    # redo with leading-whitespace awareness
    out = []
    for s in probe["inputs"]:
        had_leading_ws = len(s) > 0 and s[0].isspace()
        t = re.sub(r"\s", "", s)
        if t and not had_leading_ws:
            t = t[0].upper() + t[1:].lower()
        elif t:
            t = t.lower()
        out.append(t)
    return {"outputs": out}

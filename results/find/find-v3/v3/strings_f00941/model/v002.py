def predict(probe):
    # f(x) = x + "ny", except whitespace-only inputs become just "ny" [E1, E2]
    #   - "  " -> "ny" (whitespace stripped/ignored) [E2]
    #   - "" -> "ny" [E2]
    #   - non-whitespace content is preserved verbatim, then "ny" appended [E1, E2]
    #   - case, digits, symbols untouched [E1, E2]
    out = []
    for x in probe["inputs"]:
        if x.strip() == "":
            out.append("ny")
        else:
            out.append(x + "ny")
    return {"outputs": out}

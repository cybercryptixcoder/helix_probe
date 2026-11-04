def predict(probe):
    # Remove all whitespace [E6, E10]
    # Lowercase everything, then uppercase only the first char [E1-E11]
    # Capitalization skipped if original input starts with whitespace [E1, E2, E6, E9]
    # Unicode letters handled like ASCII by Python's str.lower/upper [E12]
    # BUT: 'İ'.lower() gives 'i̇' (i + combining dot); box keeps 'İ' unchanged [E12]
    #   -> box's lowercase does not decompose İ; treat İ as unchanged by lower()
    results = []
    for x in probe["inputs"]:
        s = "".join(ch for ch in x if not ch.isspace())
        # lowercase, but preserve İ (U+0130) as-is
        s = "".join(ch if ch == "\u0130" else ch.lower() for ch in s)
        if x and x[0].isspace():
            out = s
        elif s:
            out = s[0].upper() + s[1:]
        else:
            out = ""
        results.append(out)
    return {"outputs": results}

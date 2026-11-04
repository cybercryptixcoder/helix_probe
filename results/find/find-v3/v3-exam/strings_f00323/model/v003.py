def predict(probe):
    # The box removes all whitespace (spaces, tabs, newlines) then reverses [E2, E4].
    # E4: "a\tb"->"ba", "a\nb"->"ba", "a\t b"->"ba", "a b\tc"->"cba" — all whitespace dropped.
    # E2: "abc DEF"->"FEDcba", "x y z"->"zyx" — spaces dropped, then reversed.
    import re
    return {"outputs": [re.sub(r"\s", "", s)[::-1] for s in probe["inputs"]]}

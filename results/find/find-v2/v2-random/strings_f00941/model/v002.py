def predict(probe):
    # Appends "ny" to every input string [E1, E2, E3]
    # Leading spaces are stripped from the input before appending [E4]
    # Trailing spaces are preserved [E2, E3, E4]
    # Other content (case, digits, symbols, internal spaces) unchanged [E1-E4]
    return {"outputs": [s.lstrip() + "ny" for s in probe["inputs"]]}

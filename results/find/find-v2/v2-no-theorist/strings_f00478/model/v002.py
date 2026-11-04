def predict(probe):
    # Removes all whitespace characters (space, tab, newline, etc.) [E1, E2]
    # Multiple consecutive whitespace all deleted, not collapsed [E2]
    # Leading/trailing whitespace removed [E2]
    # Other characters (letters, digits, case, symbols) unchanged [E1]
    import re
    return {"outputs": [re.sub(r"\s", "", s) for s in probe["inputs"]]}

def predict(probe):
    # Removes all whitespace (spaces, tabs, newlines), not just ordinary spaces [E2]
    # Other characters (digits, punctuation, case) are untouched [E1, E2]
    import re
    return {"outputs": [re.sub(r"\s", "", s) for s in probe["inputs"]]}

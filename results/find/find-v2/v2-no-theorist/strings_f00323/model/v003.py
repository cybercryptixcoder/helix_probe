def predict(probe):
    # Reverse the whole string [E1, E2, E3]
    # Remove ALL whitespace characters (spaces, tabs, newlines) [E4]
    import re
    return {"outputs": [re.sub(r"\s", "", s[::-1]) for s in probe["inputs"]]}

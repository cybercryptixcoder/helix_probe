import re

def predict(probe):
    # Removes all whitespace (spaces, tabs, newlines) [E1, E2]
    # Preserves hyphens, punctuation, case, digits [E2]
    return {"outputs": [re.sub(r"\s", "", s) for s in probe["inputs"]]}

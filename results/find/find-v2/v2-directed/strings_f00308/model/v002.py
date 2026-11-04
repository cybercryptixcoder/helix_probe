import re

def predict(probe):
    # Removes all whitespace (spaces, tabs, newlines), not just spaces [E1, E2]
    # Case, digits, and symbols pass through unchanged [E1, E2]
    return {"outputs": [re.sub(r"\s", "", s) for s in probe["inputs"]]}

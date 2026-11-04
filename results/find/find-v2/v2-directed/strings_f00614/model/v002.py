import re

def predict(probe):
    # Removes all whitespace (spaces, tabs, newlines) [E1, E2]
    # Appends "F" to the result [E1, E2]
    # Other characters (case, digits, punctuation) pass through unchanged [E1]
    return {"outputs": [re.sub(r"\s", "", s) + "F" for s in probe["inputs"]]}

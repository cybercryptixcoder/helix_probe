import re

def predict(probe):
    # Removes all whitespace (spaces, tabs, newlines) [E1, E2]
    # Appends "F" to the result [E1, E2]
    # Empty / all-whitespace strings become "F" [E2]
    return {"outputs": [re.sub(r"\s", "", s) + "F" for s in probe["inputs"]]}

import re

def predict(probe):
    # Removes all whitespace characters (space, tab, newline, etc.) [E1, E2]
    # Multiple/leading/trailing whitespace all removed [E2]
    # Non-whitespace chars (digits, symbols, case) preserved [E1, E2]
    return {"outputs": [re.sub(r"\s+", "", s) for s in probe["inputs"]]}

import re

def predict(probe):
    # Removes all whitespace characters (spaces, tabs, newlines, carriage returns,
    # non-breaking spaces, etc.) from the input string [E1, E2]
    # Other characters (letters, digits, symbols, case) are preserved unchanged [E1]
    return {"outputs": [re.sub(r"\s", "", s) for s in probe["inputs"]]}

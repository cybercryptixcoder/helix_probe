import re

def predict(probe):
    # Removes all whitespace (spaces, tabs, etc.), not just single spaces [E2: "a\tb"->"ab", "a  b"->"ab", "  spaced  "->"spaced"]
    # Preserves case, digits, symbols, punctuation unchanged [E1, E2]
    # No other transformation observed [E1, E2]
    return {"outputs": [re.sub(r"\s+", "", s) for s in probe["inputs"]]}

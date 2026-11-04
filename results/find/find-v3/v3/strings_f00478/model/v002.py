def predict(probe):
    # Removes all whitespace (spaces, tabs, newlines) [E1, E2: "a\tb"->"ab", "a\nb"->"ab", "a b"->"ab"]
    # Leading/trailing whitespace also removed [E1: " Zebralower"->"Zebralower", E2: " a"->"a", "a "->"a", " "->""]
    # Non-whitespace characters preserved in order [E1: "abc123","level","bananaUPPER","Zebra" unchanged]
    import re
    return {"outputs": [re.sub(r"\s+", "", s) for s in probe["inputs"]]}

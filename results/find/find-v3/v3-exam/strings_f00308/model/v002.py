import re

def predict(probe):
    # Removes all whitespace characters (spaces, tabs, newlines, \r) [E2]
    # Leading/trailing whitespace also removed [E1, E2]
    # Everything else unchanged [E1]
    return {"outputs": [re.sub(r"\s", "", s) for s in probe["inputs"]]}

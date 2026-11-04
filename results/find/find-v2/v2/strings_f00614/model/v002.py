import re

def predict(probe):
    # Removes all whitespace (spaces, tabs, newlines) everywhere [E1, E2]
    # Appends "F" to the result [E1, E2]
    # Case preserved [E1]
    # Digits and symbols preserved [E1]
    out = []
    for s in probe.get("inputs", []):
        out.append(re.sub(r"\s+", "", s) + "F")
    return {"outputs": out}

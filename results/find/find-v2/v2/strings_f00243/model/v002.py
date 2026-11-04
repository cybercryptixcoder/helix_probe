import re

def predict(probe):
    # Remove all whitespace (spaces, tabs, newlines) first [E1, E2, E4, E6]
    # Then insert 'Z' at floor(len/2) of the whitespace-stripped string [E1-E6]
    out = []
    for s in probe.get("inputs", []):
        t = re.sub(r"\s", "", s)
        k = len(t) // 2
        out.append(t[:k] + "Z" + t[k:])
    return {"outputs": out}

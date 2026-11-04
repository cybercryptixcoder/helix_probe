import re

def predict(probe):
    # Remove all whitespace (spaces, tabs, newlines, \r) [E4]
    # Then insert 'Z' at index floor(len/2) [E1-E4]
    out = []
    for s in probe["inputs"]:
        t = re.sub(r"\s", "", s)
        i = len(t) // 2
        out.append(t[:i] + "Z" + t[i:])
    return {"outputs": out}

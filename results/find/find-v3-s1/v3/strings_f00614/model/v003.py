import re

def predict(probe):
    # Removes all whitespace (spaces, tabs, newlines) [E1, E2]
    # Appends "F" to the result [E1, E2]
    # Empty / all-whitespace strings become "F" [E2]
    # Exception: if the result (before appending F) is exactly "ABCDEF", no "F" is appended [E4]
    out = []
    for s in probe["inputs"]:
        r = re.sub(r"\s", "", s)
        if r == "ABCDEF":
            out.append(r)
        else:
            out.append(r + "F")
    return {"outputs": out}

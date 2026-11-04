import re

def predict(probe):
    # Remove all whitespace (spaces, tabs, newlines) [E1, E2]
    # Append "F" to the result [E1, E2]
    # But: if the result already ends with "F", do NOT append another "F" [E6]
    #   - "F" -> "F" (not "FF"), "FF" -> "FF" (not "FFF"), " F " -> "F" (not "FF")
    #   - "F1" -> "F1F" (doesn't end in F, so append), "1F" -> "1F" (ends in F, no append)
    # Other characters pass through unchanged [E1, E3, E4, E5]
    out = []
    for s in probe["inputs"]:
        r = re.sub(r"\s", "", s)
        if not r.endswith("F"):
            r = r + "F"
        out.append(r)
    return {"outputs": out}

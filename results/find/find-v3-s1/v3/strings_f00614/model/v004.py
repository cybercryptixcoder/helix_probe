import re

def predict(probe):
    # Removes all whitespace [E2]
    # Appends "F" unless the result already ends with "F" [E4, E6]
    #   - "ABCDEF" -> "ABCDEF" (ends with F) [E4, E6]
    #   - "XABCDEF" -> "XABCDEF" (ends with F) [E6]
    #   - "BCDEF" -> "BCDEF" (ends with F) [E6]
    #   - "ABCDEFG" -> "ABCDEFGF" (doesn't end with F) [E6]
    #   - "ABCDEFX" -> "ABCDEFXF" (doesn't end with F) [E6]
    #   - "ABCDEF ABCDEF" -> "ABCDEFABCDEF" (ends with F) [E6]
    # Empty / all-whitespace -> "F" [E2]
    out = []
    for s in probe["inputs"]:
        r = re.sub(r"\s", "", s)
        if r.endswith("F"):
            out.append(r)
        else:
            out.append(r + "F")
    return {"outputs": out}

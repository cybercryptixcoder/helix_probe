def predict(probe):
    # Hypothesis: f repeatedly removes leading characters that are 'H' or ' ' [E1, E2]
    #   - " Zebralower" -> "Zebralower" [E1]
    #   - "Hello World..." -> "ello World..." [E1]
    #   - "  Zebra" -> "Zebra" (two spaces removed) [E2]
    #   - "HH" -> "" (both H's removed) [E2]
    #   - "HZebra" -> "Zebra" [E2]
    #   - "H" -> "", " " -> "" [E2]
    # Only leading H/space are affected; interior ones untouched [E1, E2]
    out = []
    for s in probe["inputs"]:
        i = 0
        while i < len(s) and s[i] in ("H", " "):
            i += 1
        out.append(s[i:])
    return {"outputs": out}

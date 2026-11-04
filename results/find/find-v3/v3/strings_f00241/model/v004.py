def predict(probe):
    # Identity on ordinary strings [E1, E2, E3, E4, E5, E7, E9, E11, E13]
    # Uppercase 'D' -> 'J' anywhere in the string [E6, E8, E10, E12, E14]
    #   lowercase 'd' unchanged [E6, E12]
    # Uppercase 'B' -> '' (deleted) [E14: "B0RG"->"0RG"]
    #   (only evidence is B0RG; assume B is deleted wherever it appears)
    out = []
    for s in probe["inputs"]:
        s = s.replace("D", "J")
        s = s.replace("B", "")
        out.append(s)
    return {"outputs": out}

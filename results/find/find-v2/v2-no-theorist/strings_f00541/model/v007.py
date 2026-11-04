def predict(probe):
    # Every 'H' anywhere is removed [E2, E5, E6]
    # Whitespace (spaces, tabs, newlines, CR, VT, FF) is stripped from both ends [E2, E3, E4, E8]
    # But a string that is entirely whitespace (after H-removal) is left unchanged [E6 "H H"->" ", E8 "H\nH"->"\n"]
    # Other uppercase letters are NOT removed [E4]
    # Order: remove H first, then strip whitespace [E6, E8]
    out = []
    for s in probe["inputs"]:
        t = s.replace("H", "")
        stripped = t.strip()
        if stripped == "" and t != "":
            out.append(t)
        else:
            out.append(stripped)
    return {"outputs": out}

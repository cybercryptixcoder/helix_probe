def predict(probe):
    # Every 'H' anywhere is removed [E2, E5, E6]
    # Whitespace (spaces, tabs, newlines, CR, VT, FF) is stripped from both ends [E2, E3, E4, E8]
    # Order: strip whitespace FIRST, then remove H [E10: "H apple"->" apple", "apple H"->"apple "]
    #   (H removal happens after stripping, so whitespace exposed by H-removal is NOT stripped)
    # A string that is entirely whitespace is left unchanged [E6 "H H"->" ", E8 "H\nH"->"\n"]
    #   Note: "H H" strips to "H H" (interior space kept), then H-removal gives " "
    # Other uppercase letters are NOT removed [E4]
    out = []
    for s in probe["inputs"]:
        stripped = s.strip()
        out.append(stripped.replace("H", ""))
    return {"outputs": out}

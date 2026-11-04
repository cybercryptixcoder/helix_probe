def predict(probe):
    # Every 'H' anywhere is removed [E2, E5, E6]
    # Whitespace (spaces, tabs) is stripped from both ends [E2, E3, E4]
    # Other uppercase letters are NOT removed [E4]
    # Order: remove H first, then strip whitespace [E6: "H H"->" "]
    out = []
    for s in probe["inputs"]:
        out.append(s.replace("H", "").strip())
    return {"outputs": out}

def predict(probe):
    # Leading whitespace (spaces, tabs) is stripped [E2, E4]
    # Leading 'H' is stripped, repeatedly [E2: "HH"->"", "HHHapple"->"apple"]
    # Trailing whitespace (spaces, tabs) is stripped [E3, E4]
    # Other leading uppercase letters (A, B, Z) are NOT stripped [E4]
    # Interior 'H' is also stripped: "Hello World"->"ello World",
    #   "function Hello World"->"function ello World" [E1, E2, E5]
    #   i.e. every 'H' anywhere is removed, not just leading ones
    out = []
    for s in probe["inputs"]:
        s = s.replace("H", "")
        out.append(s.strip())
    return {"outputs": out}

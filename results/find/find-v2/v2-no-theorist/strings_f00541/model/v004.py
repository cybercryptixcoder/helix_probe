def predict(probe):
    # Leading whitespace (spaces, tabs, etc.) is stripped [E2, E4]
    # Leading 'H' is stripped, repeatedly [E2: "HH"->"", "HHHapple"->"apple"]
    # Trailing whitespace (spaces, tabs) is stripped [E3, E4]
    # Other leading uppercase letters (A, B, Z) are NOT stripped [E4]
    # Interior characters untouched [E1, E2, E3]
    out = []
    for s in probe["inputs"]:
        i = 0
        while i < len(s) and (s[i] in ("H",) or s[i].isspace()):
            i += 1
        out.append(s[i:].rstrip())
    return {"outputs": out}

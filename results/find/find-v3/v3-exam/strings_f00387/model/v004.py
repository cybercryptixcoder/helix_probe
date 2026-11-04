def predict(probe):
    # Rule: delete ALL lowercase 'm' characters, then str.capitalize() [E4: "mm"->"", "mM"->"M"]
    # Uppercase 'M' is untouched [E4: "M"->"M", "MM"->"Mm", "aM"->"Am", "Ma"->"Ma", "Mm"->"M"]
    # capitalize() lowercases the rest and uppercases first char [E1, E2, E3]
    out = []
    for s in probe["inputs"]:
        s = s.replace("m", "")
        out.append(s.capitalize())
    return {"outputs": out}

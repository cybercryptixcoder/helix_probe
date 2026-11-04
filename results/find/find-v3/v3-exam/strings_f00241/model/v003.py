def predict(probe):
    # Identity for most inputs [E1, E2, E3, E4, E7]
    # Every uppercase 'D' anywhere in the string becomes 'J' [E5, E6, E8]
    out = []
    for s in probe["inputs"]:
        out.append(s.replace("D", "J"))
    return {"outputs": out}

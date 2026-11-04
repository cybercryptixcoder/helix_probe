def predict(probe):
    # Uppercase D -> J everywhere [E5,E6,E8,E12,E14]
    # Uppercase B is deleted everywhere [E16]
    # Other characters unchanged [E1-E15,E16]
    out = []
    for s in probe["inputs"]:
        out.append(s.replace("D", "J").replace("B", ""))
    return {"outputs": out}

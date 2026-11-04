def predict(probe):
    # Rules (revised after E9):
    # 1. Remove all spaces [E1-E8]
    # 2. Remove all tab characters too [E9: "worldtab\tsep" -> "worldtabsep"]
    # 3. Insert 'Z' at middle index (len//2) of the cleaned string [E1-E9]
    out = []
    for s in probe.get("inputs", []):
        t = s.replace(" ", "").replace("\t", "")
        m = len(t) // 2
        out.append(t[:m] + "Z" + t[m:])
    return {"outputs": out}

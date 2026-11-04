def predict(probe):
    # Identity on ordinary strings [E1, E2, E3, E4]
    # Exception: a final 'D' at end of string becomes 'J' [E5: "aMiXeD" -> "aMiXeJ"]
    #   (only observed at end; uncertain whether it's end-only or any D — marked ?)
    out = []
    for s in probe["inputs"]:
        if s.endswith("D"):
            s = s[:-1] + "J"
        out.append(s)
    return {"outputs": out}

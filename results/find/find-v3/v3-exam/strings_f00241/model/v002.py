def predict(probe):
    # Identity for most inputs [E1, E2, E3, E4]
    # Exception: trailing "D" becomes "J" in some cases [E5: "aMiXeD" -> "aMiXeJ"]
    # Hypothesis: a final uppercase 'D' is replaced by 'J' [E5]
    # (Only one data point; other 'D'-ending inputs untested. Marked ?)
    out = []
    for s in probe["inputs"]:
        if s.endswith("D"):
            s = s[:-1] + "J"
        out.append(s)
    return {"outputs": out}

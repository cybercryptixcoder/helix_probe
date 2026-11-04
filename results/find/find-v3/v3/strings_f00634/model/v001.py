def predict(probe):
    # Capitalize first char, lowercase rest, then remove all spaces [E1]
    out = []
    for s in probe["inputs"]:
        if s:
            s = s[0].upper() + s[1:].lower()
        s = s.replace(" ", "")
        out.append(s)
    return {"outputs": out}

def predict(probe):
    # Strip ALL leading spaces [E4]
    # Remove ALL 'H' characters everywhere [E4, E5, E6]
    # Strip ALL trailing spaces [E3, E4]
    # Order: leading spaces, then remove H's, then trailing spaces [E4: " H"->""]
    # Lowercase 'h' survives [E6]
    out = []
    for s in probe["inputs"]:
        s = s.lstrip(" ")
        s = s.replace("H", "")
        s = s.rstrip(" ")
        out.append(s)
    return {"outputs": out}

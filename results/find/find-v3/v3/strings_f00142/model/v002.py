def predict(probe):
    # Each char shifted +5 in ASCII [E1-E4]
    # Then "W" appended [E1-E4]
    # Exception: if the shifted string already ends with "W", don't append another [E4: "lowerUPPER" -> "qt|jwZUUJW" not "...WW"]
    out = []
    for s in probe["inputs"]:
        shifted = "".join(chr(ord(c) + 5) for c in s)
        if shifted.endswith("W"):
            out.append(shifted)
        else:
            out.append(shifted + "W")
    return {"outputs": out}

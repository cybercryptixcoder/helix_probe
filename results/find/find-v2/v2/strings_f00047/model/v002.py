def predict(probe):
    # Only the very first character is capitalized (if alphabetic); everything else lowercased [E1, E2]
    # If first char is not alphabetic, nothing is capitalized [E2: "123abc"->"123abc", "!hello"->"!hello", "  two words"->"  two words"]
    # Leading spaces preserved, no capitalization of later words [E1, E2]
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append(s)
            continue
        t = s.lower()
        if t[0].isalpha():
            t = t[0].upper() + t[1:]
        out.append(t)
    return {"outputs": out}

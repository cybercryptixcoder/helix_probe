def predict(probe):
    # Reverse each word (character order within each token) [E1, E2, E3]
    # Word order preserved [E2: "dog house"->"god esuoh"]
    # Whitespace runs collapse to single spaces; ends stripped [E4, E10]
    # Append "I" at the very end, but if the result already ends with "I", don't double it [E12]
    #   E12: "I"->"I", "hi I"->"ih I", "III"->"III", "Iii"->"iiI", "end I"->"dne I"
    #   i.e. append "I" only if the reversed string doesn't already end in "I"
    out = []
    for s in probe.get("inputs", []):
        try:
            parts = s.split()
            rev = " ".join(p[::-1] for p in parts)
            if not rev.endswith("I"):
                rev += "I"
            out.append(rev)
        except Exception:
            out.append("I")
    return {"outputs": out}

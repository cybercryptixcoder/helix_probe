def predict(probe):
    # f reverses each whitespace-separated token, rejoins with single spaces [E2,E3,E4,E5]
    # then appends "I" — but only if the result doesn't already end with "I" [E6]
    # Evidence: "I"->"I", "II"->"II", "I I"->"I I", "Iabc"->"cbaI" (not cbaII),
    #   "Ih"->"hI" (not hII), "I I I"->"I I I", "abcI"->"IcbaI", "HI"->"IHI" [E6]
    # So the suffix is a marker: append "I" unless the transformed string already ends in "I".
    out = []
    for s in probe["inputs"]:
        words = s.split()
        r = " ".join(w[::-1] for w in words)
        if not r.endswith("I"):
            r += "I"
        out.append(r)
    return {"outputs": out}

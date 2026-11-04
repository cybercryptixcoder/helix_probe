def predict(probe):
    # f reverses each whitespace-separated word in place, preserving word order,
    # then appends "I" [E1: "hello"->"ollehI", "a b"->"a bI"; E2: "ab cd"->"ba dcI"]
    # Leading/trailing/multiple whitespace collapses to single spaces [E2, E3]
    # Single chars unchanged, empty -> "I" [E1]
    # Case preserved [E1: "Hello"->"olleHI"; E2: "Ab Cd Ef"->"bA dC fEI"]
    # The trailing "I" is appended with no separator [E1, E2, E5]
    # BUT: if the transformed result already ends in "I", no extra "I" is added
    #   [E5: "I"->"I", "II"->"II", "x I"->"x I"]  -- i.e. append "I" only if not already ending in "I"
    def rev_word(w):
        return w[::-1]
    out = []
    for x in probe["inputs"]:
        words = x.split()
        s = " ".join(rev_word(w) for w in words)
        if not s.endswith("I"):
            s += "I"
        out.append(s)
    return {"outputs": out}

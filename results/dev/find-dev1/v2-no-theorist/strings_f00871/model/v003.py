def predict(probe):
    # Split on any whitespace run, reverse each token, join with single space, append "I" [E1-E5]
    # "ab"->"baI", "a b"->"a bI", "ab cd"->"ba dcI" [E1,E2]
    # Internal whitespace runs collapse to one space [E3,E4,E5]
    # Leading/trailing whitespace stripped [E1,E2,E3]
    # Empty/whitespace-only -> "I" [E1,E3]
    out = []
    for s in probe.get("inputs", []):
        toks = s.split()
        out.append(" ".join(t[::-1] for t in toks) + "I")
    return {"outputs": out}

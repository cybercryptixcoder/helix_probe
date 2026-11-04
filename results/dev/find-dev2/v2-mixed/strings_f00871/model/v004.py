def predict(probe):
    # Reverse each word (character order within each token) [E1, E2, E3]
    # Word order preserved [E2: "dog house"->"god esuoh"]
    # Whitespace is normalized: all runs of whitespace (spaces, tabs) collapse to single spaces [E4]
    # Leading and trailing whitespace is stripped [E4: " a b "->"a b", "  leading"->"gnidael"]
    # Append "I" at the very end [E1, E2, E3]
    # So: s.split() (default, splits on any whitespace, drops empties), reverse each token, join with " ", append "I"
    out = []
    for s in probe.get("inputs", []):
        try:
            parts = s.split()
            rev = " ".join(p[::-1] for p in parts)
            out.append(rev + "I")
        except Exception:
            out.append("I")
    return {"outputs": out}

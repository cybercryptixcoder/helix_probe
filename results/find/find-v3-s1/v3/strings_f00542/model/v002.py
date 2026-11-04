def predict(probe):
    # Reverse each word's characters, keep word order [E1, E2, E3]
    # Split on runs of spaces; multiple spaces collapse to one [E4: "ab  cd"->"ba dc", "a  b"->"a b"]
    # Leading/trailing spaces are dropped [E4: "  ab"->"ba", "ab  "->"ba"]
    # So effectively: split on whitespace, reverse each token, join with single spaces
    out = []
    for s in probe["inputs"]:
        out.append(" ".join(w[::-1] for w in s.split()))
    return {"outputs": out}

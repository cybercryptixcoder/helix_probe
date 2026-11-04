def predict(probe):
    # Hypothesis: f reverses the order of whitespace-separated words [E1]
    # "Hello World function lazy" -> "lazy function World Hello" [E1]
    # Single words unchanged: "abc123", "level", "Zebra", "bananaUPPER" [E1]
    # Leading space stripped: " Zebralower" -> "Zebralower" [E1]
    # ? Likely split on whitespace and rejoin with single spaces
    out = []
    for s in probe["inputs"]:
        words = s.split()
        out.append(" ".join(reversed(words)))
    return {"outputs": out}

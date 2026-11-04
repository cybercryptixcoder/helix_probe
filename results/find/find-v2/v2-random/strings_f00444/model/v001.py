def predict(probe):
    # Reverses the order of whitespace-separated words [E1: "Hello World function lazy" -> "lazy function World Hello"]
    # Preserves single tokens unchanged [E1: "abc123", "level", "bananaUPPER", "Zebra"]
    # Leading space is dropped [E1: " Zebralower" -> "Zebralower"]
    # ? Assumes split on whitespace and rejoin with single spaces
    out = []
    for s in probe["inputs"]:
        words = s.split()
        out.append(" ".join(reversed(words)))
    return {"outputs": out}

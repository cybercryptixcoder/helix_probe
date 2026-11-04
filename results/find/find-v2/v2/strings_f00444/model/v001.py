def predict(probe):
    # Rule: reverse the order of whitespace-separated words [E1]
    # Evidence: "Hello World function lazy" -> "lazy function World Hello" [E1]
    # Rule: strip leading/trailing whitespace [E1]
    # Evidence: " Zebralower" -> "Zebralower" [E1]
    # Rule: single tokens unchanged (no reordering possible) [E1]
    # Evidence: "abc123","level","bananaUPPER","Zebra" unchanged [E1]
    # ?: likely split on whitespace, reverse, join with single space
    out = []
    for s in probe.get("inputs", []):
        try:
            words = s.split()
            out.append(" ".join(reversed(words)))
        except Exception:
            out.append(s)
    return {"outputs": out}

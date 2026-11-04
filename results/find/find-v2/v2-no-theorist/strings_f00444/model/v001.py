def predict(probe):
    # Observations [E1]:
    # - "abc123" -> "abc123" (unchanged)
    # - "level" -> "level" (unchanged)
    # - " Zebralower" -> "Zebralower" (leading space stripped)
    # - "Hello World function lazy" -> "lazy function World Hello" (words reversed)
    # - "bananaUPPER" -> "bananaUPPER" (unchanged)
    # - "Zebra" -> "Zebra" (unchanged)
    # Hypothesis: strip leading/trailing whitespace, then reverse the order of
    # whitespace-separated words. Single words are unaffected by reversal.
    # ? Whether internal whitespace runs are collapsed or preserved is unknown.
    out = []
    for s in probe.get("inputs", []):
        try:
            words = s.split()
            out.append(" ".join(reversed(words)))
        except Exception:
            out.append(s)
    return {"outputs": out}

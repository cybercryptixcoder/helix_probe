def predict(probe):
    # Observations [E1]:
    # - "abc123" -> "abc123" (unchanged)
    # - "level" -> "level" (unchanged, palindrome)
    # - " Zebralower" -> "Zebralower" (leading space removed)
    # - "Hello World function lazy" -> "lazy function World Hello" (words reversed)
    # - "bananaUPPER" -> "bananaUPPER" (unchanged)
    # - "Zebra" -> "Zebra" (unchanged)
    #
    # Hypothesis: strip leading/trailing whitespace, then if the string contains
    # a space (multiple words), reverse the order of the words. Otherwise return
    # the stripped string unchanged.
    out = []
    for s in probe["inputs"]:
        t = s.strip()
        if " " in t:
            t = " ".join(t.split(" ")[::-1])
        out.append(t)
    return {"outputs": out}

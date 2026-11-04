def predict(probe):
    # Only one observation so far [E1]:
    # "abc123" -> "abc123" (unchanged)
    # "level" -> "level" (unchanged)
    # " Zebralower" -> "Zebralower" (leading space removed)
    # "Hello World function lazy" -> "ello World function lazy" (leading 'H' removed)
    # "bananaUPPER" -> "bananaUPPER" (unchanged)
    # "Zebra" -> "Zebra" (unchanged)
    # Hypothesis (?): remove the first character if it is uppercase 'H' or a space.
    # This is a weak guess from a single experiment; many other rules fit.
    out = []
    for s in probe["inputs"]:
        if s[:1] in ("H", " "):
            out.append(s[1:])
        else:
            out.append(s)
    return {"outputs": out}

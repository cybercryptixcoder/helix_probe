def predict(probe):
    # Observations:
    # "Hello World function lazy" -> "ello World function lazy" (H removed)
    # "function Hello World" -> "function ello World" (H removed, not first char!)
    # "test case" -> "test case" (unchanged)
    # " Zebralower" -> "Zebralower" (leading space stripped)
    # "banana data banana " -> "banana data banana" (trailing space stripped)
    # "Example " -> "Example" (trailing space stripped)
    # "banana a data " -> "banana a data" (trailing space stripped)
    # "Example123","abc123","level","bananaUPPER","Zebra","lazy","banana",
    #   "world42","racecar Example racecar","aMiXeD" -> unchanged
    #
    # Rule 1: strip leading/trailing whitespace [E1,E2,E3]
    # Rule 2: remove the first uppercase letter 'H' that appears at a word
    #   boundary? "Hello World function lazy" -> H at start removed.
    #   "function Hello World" -> H after space removed.
    #   "test case" no H -> unchanged. "Example123" no H -> unchanged.
    #   "Zebra" no H -> unchanged. "bananaUPPER" no H -> unchanged.
    #   "racecar Example racecar" no H -> unchanged.
    #   Hypothesis: remove the first 'H' character in the string [E1,E3].
    #   Check: "Hello World function lazy" first H at index 0 -> removed. Good.
    #   "function Hello World" first H at index 9 -> removed. Good.
    #   No other evidence has an H. Plausible: delete first 'H'.
    out = []
    for s in probe["inputs"]:
        s = s.strip()
        i = s.find("H")
        if i != -1:
            s = s[:i] + s[i+1:]
        out.append(s)
    return {"outputs": out}

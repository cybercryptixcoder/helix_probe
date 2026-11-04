def predict(probe):
    # Rule: strip one leading space if present [E1: " Zebralower"->"Zebralower"; E2: " Hello"->"ello", " He"->"e", "  two spaces"->"two spaces"]
    # Rule: after that, strip one leading "H" if present [E2: "H"->"", "He"->"e", "Hello"->"ello", "Hi there"->"i there", "Habc"->"abc", "H H"->" ", "Help"->"elp"; E1: "Hello World..."->"ello World..."]
    # Rule: otherwise unchanged [E1: abc123, level, bananaUPPER, Zebra]
    out = []
    for s in probe["inputs"]:
        if s.startswith(" "):
            s = s[1:]
        if s.startswith("H"):
            s = s[1:]
        out.append(s)
    return {"outputs": out}

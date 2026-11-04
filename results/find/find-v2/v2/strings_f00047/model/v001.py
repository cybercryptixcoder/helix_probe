def predict(probe):
    # Capitalize first letter, lowercase the rest [E1: "abc123"->"Abc123", "level"->"Level",
    #   "Hello World function lazy"->"Hello world function lazy", "bananaUPPER"->"Bananaupper"]
    # Leading space preserved, first non-space char capitalized, rest lowercased [E1: " Zebralower"->" zebralower"]
    # "Zebra"->"Zebra" consistent with capitalize-then-lowercase [E1]
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append(s)
            continue
        # find first alphabetic char to capitalize, lowercase everything else
        chars = list(s.lower())
        for i, c in enumerate(chars):
            if c.isalpha():
                chars[i] = c.upper()
                break
        out.append("".join(chars))
    return {"outputs": out}

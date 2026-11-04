def predict(probe):
    # Reverse the string, then swap case [E1: "abc123"->"321cba", "level"->"Level",
    #   " Zebralower"->"Rewolarbez ", "Hello World function lazy"->"Yzal noitcnuf dlrow olleh",
    #   "bananaUPPER"->"Reppuananab", "Zebra"->"Arbez"]
    # Order: reverse first, then swap case (case swap is position-independent so order doesn't matter here).
    out = []
    for s in probe["inputs"]:
        r = s[::-1]
        r = r.swapcase()
        out.append(r)
    return {"outputs": out}

def predict(probe):
    # Capitalize first letter of each word, lowercase the rest [E1]
    # "abc123"->"Abc123", "level"->"Level", " Zebralower"->" zebralower"
    # "Hello World function lazy"->"Hello world function lazy"
    # "bananaUPPER"->"Bananaupper", "Zebra"->"Zebra"
    # Leading space preserved; words split on whitespace, each word capitalized
    def cap_word(w):
        if not w:
            return w
        return w[0].upper() + w[1:].lower()
    out = []
    for s in probe["inputs"]:
        # split preserving whitespace runs
        import re
        parts = re.split(r'(\s+)', s)
        res = []
        for p in parts:
            if p and not p.isspace():
                res.append(cap_word(p))
            else:
                res.append(p)
        out.append("".join(res))
    return {"outputs": out}

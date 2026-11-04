def predict(probe):
    # Capitalize first letter of each word, lowercase the rest [E1]
    # "abc123"->"Abc123", "level"->"Level", " Zebralower"->" zebralower"
    # "Hello World function lazy"->"Hello world function lazy"
    # "bananaUPPER"->"Bananaupper", "Zebra"->"Zebra"
    # Note: leading space preserved, so capitalize each whitespace-separated token
    def cap_word(w):
        if not w:
            return w
        return w[0].upper() + w[1:].lower()
    outs = []
    for s in probe["inputs"]:
        # Split on spaces preserving them, capitalize each token
        parts = s.split(" ")
        outs.append(" ".join(cap_word(p) for p in parts))
    return {"outputs": outs}

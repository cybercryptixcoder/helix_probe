def predict(probe):
    # Lowercase the whole string, then capitalize the first character [E1]
    # "abc123"->"Abc123", "level"->"Level", " Zebralower"->" zebralower"
    # "Hello World function lazy"->"Hello world function lazy"
    # "bananaUPPER"->"Bananaupper", "Zebra"->"Zebra"
    out = []
    for s in probe["inputs"]:
        t = s.lower()
        if t:
            t = t[0].upper() + t[1:]
        out.append(t)
    return {"outputs": out}

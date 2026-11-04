def predict(probe):
    # Reverse the string, lowercase everything, then uppercase the first char [E1, E2]
    # E1: "abc123"->"321cba", "level"->"Level", " Zebralower"->"Rewolarbez "
    # E2: "Example123"->"321elpmaxe", "test case"->"Esac tset", "lazy"->"Yzal"
    out = []
    for s in probe["inputs"]:
        r = s[::-1].lower()
        if r:
            r = r[0].upper() + r[1:]
        out.append(r)
    return {"outputs": out}

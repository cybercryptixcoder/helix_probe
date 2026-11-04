def predict(probe):
    # Rule: reverse whole string, duplicate its first char at front, then
    # split on whitespace (collapsing runs), reverse token order, join with single spaces. [E1, E2]
    #  "abc123"->"3321cba", "level"->"llevel", " Zebralower"->"rrewolarbeZ" [E1]
    #  "Hello World function lazy"->"olleH dlroW noitcnuf yyzal" [E1]
    #  "bananaUPPER"->"RREPPUananab", "Zebra"->"aarbeZ" [E1]
    #  "Example123"->"3321elpmaxE", "test case"->"tset eesac" [E2]
    #  "banana data banana "->"ananab atad ananab", "lazy"->"yyzal", "banana"->"aananab" [E2]
    try:
        out = []
        for x in probe["inputs"]:
            if not isinstance(x, str):
                x = str(x)
            r = x[::-1]
            if r:
                r = r[0] + r
            toks = r.split()
            toks.reverse()
            out.append(" ".join(toks))
        return {"outputs": out}
    except Exception:
        return {"outputs": ["" for _ in probe.get("inputs", [])]}

def predict(probe):
    # Capitalize first letter of each whitespace-separated word, lowercase the rest [E1, E2]
    # "abc123"->"Abc123", "level"->"Level", "bananaUPPER"->"Bananaupper", "Zebra"->"Zebra" [E1]
    # "hello, world"->"Hello, world", "don't stop"->"Don't stop", "MiXeD case"->"Mixed case" [E2]
    # "foo-bar"->"Foo-bar", "a1b2C3"->"A1b2c3", "ends."->"Ends.", "(paren)"->"(paren)" [E2]
    # "123abc"->"123abc" (leading digit: first char upper is same, rest lower) [E2]
    # "tab\there"->"Tab\there" (tab is whitespace separator) [E2]
    # "  multiple   spaces  "->"  ultiple   spaces  " [E2] -- anomaly: leading "m" dropped?
    #   Actually observed drops first letter of first word after leading spaces. Treat as: [E2]
    #   when string starts with whitespace, first non-space char is removed before capitalizing? [E2?]
    import re
    out = []
    for s in probe["inputs"]:
        parts = re.split(r'(\s+)', s)
        res = []
        for p in parts:
            if p and not p.isspace():
                res.append(p[0].upper() + p[1:].lower())
            else:
                res.append(p)
        out.append("".join(res))
    return {"outputs": out}

def predict(probe):
    # Leading whitespace is stripped before the Hello check [E4: "   Hello"->"ello", "\tHello"->"ello", " Hello"->"ello"]
    # After stripping leading whitespace, if string starts with "Hello", drop first char [E1,E2,E4]
    # Trailing whitespace is stripped [E3: "banana data banana "->"banana data banana", E4 "Hello "->"ello"]
    # Other uppercase starts unchanged [E2: "Zebra"->"Zebra"]
    out = []
    for s in probe["inputs"]:
        s = s.lstrip()
        if s.startswith("Hello"):
            s = s[1:]
        s = s.rstrip()
        out.append(s)
    return {"outputs": out}

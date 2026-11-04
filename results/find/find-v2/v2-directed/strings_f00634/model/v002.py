def predict(probe):
    # Lowercase entire string, then uppercase only the first character [E1, E2]
    # "two Words"->"Twowords", "TWO WORDS"->"Twowords", "a b c"->"Abc" [E2]
    # "foo-bar baz"->"Foo-barbaz", "a.b c"->"A.bc" [E2]
    # Spaces removed entirely [E1, E2]
    # "  spaced  "->"spaced", "!@#$%"->"!@#$%", "12345"->"12345" [E1]
    out = []
    for s in probe.get("inputs", []):
        t = "".join(s.split()).lower()
        out.append(t[:1].upper() + t[1:])
    return {"outputs": out}

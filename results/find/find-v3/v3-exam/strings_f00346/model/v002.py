def predict(probe):
    # Rule: remove all spaces, then shift the first character by +2 in ASCII [E1, E2]
    # - "abc123"->"cbc123", "level"->"nevel", "Zebra"->"Bebra" [E1]
    # - "abc def"->"cbcdef", "Abc def"->"Cbcdef", "a b c"->"cbc" [E2]
    # - "  hello  "->"jello", "hello world"->"jelloworld" [E2]
    # Exception: if the first character (after removing spaces) is a digit,
    #   it is left unchanged [E2: "1abc"->"1abc", "123 abc"->"123abc"]
    out = []
    for s in probe["inputs"]:
        t = s.replace(" ", "")
        if t and not t[0].isdigit():
            t = chr((ord(t[0]) + 2) % 256) + t[1:]
        out.append(t)
    return {"outputs": out}

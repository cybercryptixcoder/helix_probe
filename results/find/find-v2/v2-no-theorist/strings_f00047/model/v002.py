def predict(probe):
    # Capitalize only the first character of the whole string; lowercase the rest [E1, E2]
    # "hello world"->"Hello world", "HELLO WORLD"->"Hello world" [E2]
    # "2hello"->"2hello" (leading digit: no letter to capitalize, rest lowercased) [E2]
    # "hello 2world"->"Hello 2world" (only first char of string capitalized) [E2]
    # "a b c"->"A b c" [E2]
    # "abc123"->"Abc123", "bananaUPPER"->"Bananaupper" [E1]
    # " Zebralower"->" zebralower" (leading space: first char is space, rest lowercased) [E1]
    # "Zebra"->"Zebra" [E1]
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append(s)
        else:
            out.append(s[0].upper() + s[1:].lower())
    return {"outputs": out}

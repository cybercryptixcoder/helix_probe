def predict(probe):
    # All whitespace (space, tab, newline) is removed [E6: "\thello"->"hello", "hello\tworld"->"Helloworld", "hello\nworld"->"Helloworld"]
    # After removing whitespace, the result is lowercased entirely, then:
    #   - if the ORIGINAL input starts with whitespace: no capitalization [E1 " Zebralower"->"zebralower", E6 "  HELLO"->"hello"]
    #   - otherwise: first character uppercased [E1, E3, E4, E5, E6]
    # Non-letter first chars: upper() is a no-op, so "123abc"->"123abc", "!hello"->"!hello" [E2, E6]
    # Empty / all-whitespace -> "" [E2 "  "->""]
    results = []
    for x in probe["inputs"]:
        s = "".join(ch for ch in x if not ch.isspace()).lower()
        if x and x[0].isspace():
            out = s
        elif s:
            out = s[0].upper() + s[1:]
        else:
            out = ""
        results.append(out)
    return {"outputs": results}

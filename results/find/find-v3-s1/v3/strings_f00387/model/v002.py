def predict(probe):
    # Only the first character of the whole string is uppercased; everything else lowercased [E1, E2]
    # "hello world"->"Hello world", "Hello World"->"Hello world", "test caseMiXeD"->"Test casemixed" [E1,E2]
    # Leading whitespace: first non-space char is NOT uppercased ("  leading"->"  leading") [E2]
    # If first char is a digit, it stays; rest lowercased ("123abc"->"123abc", "a1b2"->"A1b2") [E2]
    # Trailing spaces preserved ("trailing  "->"Trailing  ") [E1,E2]
    # Multiple spaces preserved ("a  b"->"A  b") [E2]
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append(s)
            continue
        first = s[0]
        if first.isspace():
            # leading whitespace: no capitalization at all, just lowercase rest
            out.append(first + s[1:].lower())
        else:
            out.append(first.upper() + s[1:].lower())
    return {"outputs": out}

def predict(probe):
    # Remove ALL whitespace (spaces, tabs, newlines) [E2: "a\tb"->"Ab", "a\nb"->"Ab"]
    # Then capitalize first letter, lowercase rest [E1, E2]
    # Leading whitespace stripped before capitalization [E2: "  apple"->"apple"]
    #   -> note: "  apple" -> "apple" (lowercase!), but " hello world" -> "helloworld"
    #      Wait: "  apple"->"apple" but " hello world"->"helloworld" (no capital).
    #      And "apple  "->"Apple" (capital). So leading whitespace prevents capitalization?
    #      "  apple" -> "apple" (no cap), " hello world" -> "helloworld" (no cap)
    #      "apple  " -> "Apple" (cap), "a  b" -> "Ab" (cap)
    #      So: if the ORIGINAL string starts with whitespace, no capitalization.
    #      Otherwise capitalize first char of whitespace-stripped result.
    # Non-letter first char: "123abc"->"123abc", "!hello"->"!hello" (unchanged, no cap) [E2]
    #   -> capitalize only applies if first char is a letter; .upper() on digit/symbol is no-op anyway
    out = []
    for s in probe["inputs"]:
        t = "".join(s.split())  # remove all whitespace
        if t:
            if s[:1].isspace():
                # leading whitespace present: no capitalization
                t = t[0].lower() + t[1:].lower()
            else:
                t = t[0].upper() + t[1:].lower()
        out.append(t)
    return {"outputs": out}

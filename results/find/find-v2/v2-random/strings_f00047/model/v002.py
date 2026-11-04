def predict(probe):
    # Capitalize first letter of the string, lowercase the rest [E1, E2]
    # "abc123" -> "Abc123" [E1]
    # "level" -> "Level" [E1]
    # "Hello World function lazy" -> "Hello world function lazy" [E1]
    # "bananaUPPER" -> "Bananaupper" [E1]
    # "test case" -> "Test case" [E2]
    # "banana data banana " -> "Banana data banana" [E2] (trailing space stripped)
    # " Zebralower" -> " zebralower" [E1] (leading space kept, no cap)
    # So: strip trailing whitespace, then capitalize first char, lowercase rest.
    out = []
    for s in probe["inputs"]:
        s = s.rstrip()
        if not s:
            out.append(s)
        else:
            out.append(s[0].upper() + s[1:].lower())
    return {"outputs": out}

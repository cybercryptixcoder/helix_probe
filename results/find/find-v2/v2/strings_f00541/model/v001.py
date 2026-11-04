def predict(probe):
    # Removes the first character if it is an uppercase letter [E1: "Hello World..." -> "ello World..."]
    # Other inputs unchanged [E1: "abc123", "level", " Zebralower", "bananaUPPER", "Zebra"]
    # " Zebralower" starts with space, unchanged; "Zebra" starts with uppercase Z but unchanged?
    # Wait: "Zebra" -> "Zebra" unchanged, but "Hello..." -> "ello...". Difference: "Hello" has lowercase after H?
    # "Zebra" also has lowercase after Z. Hmm. Maybe only removes leading uppercase if followed by lowercase AND string has space?
    # "Hello World function lazy" has spaces; "Zebra" doesn't. Rule: if starts with uppercase and contains space, drop first char.
    out = []
    for s in probe["inputs"]:
        if len(s) > 0 and s[0].isupper() and " " in s:
            out.append(s[1:])
        else:
            out.append(s)
    return {"outputs": out}

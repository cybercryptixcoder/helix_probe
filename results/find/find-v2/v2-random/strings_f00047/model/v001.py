def predict(probe):
    # Capitalize first letter of each word, lowercase the rest [E1]
    # "abc123" -> "Abc123" (digit stays, first char upper) [E1]
    # "level" -> "Level" [E1]
    # " Zebralower" -> " zebralower" (leading space preserved, first letter lowercased?) [E1]
    # "Hello World function lazy" -> "Hello world function lazy" [E1]
    # "bananaUPPER" -> "Bananaupper" [E1]
    # "Zebra" -> "Zebra" [E1]
    # So: title-case each word, but leading whitespace preserved and doesn't trigger capitalization
    def cap_word(w):
        if not w:
            return w
        return w[0].upper() + w[1:].lower()
    out = []
    for s in probe["inputs"]:
        # split preserving whitespace runs
        import re
        parts = re.split(r'(\s+)', s)
        res = []
        for p in parts:
            if p == '' or p.isspace():
                res.append(p)
            else:
                res.append(cap_word(p))
        out.append(''.join(res))
    return {"outputs": out}

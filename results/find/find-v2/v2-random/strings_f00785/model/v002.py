def predict(probe):
    # First letter of each word is shifted forward by 1 in the alphabet, case preserved [E1, E2]
    #   abc123->bbc123, level->mevely, Hello->Iello, Zebra->Aebra, Example->Fxample,
    #   test->uest, lazy->mazy, banana->canana
    # All other letters are unchanged [E1, E2]
    # Non-letters (digits, spaces, symbols) are unchanged [E1, E2]
    # A trailing 'y' is appended to every output [E1, E2]
    # 'z'/'Z' wraps to 'a'/'A' [E1: Zebra->Aebray]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 1) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 1) % 26 + ord('A'))
        return c
    outs = []
    for s in probe.get("inputs", []):
        res = []
        prev = ' '
        for c in s:
            if prev in (' ', '\t', '\n') or prev == '':
                res.append(shift(c))
            else:
                res.append(c)
            prev = c
        outs.append("".join(res) + "y")
    return {"outputs": outs}

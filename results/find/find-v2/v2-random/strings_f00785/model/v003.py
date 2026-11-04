def predict(probe):
    # Only the FIRST character of the whole string is shifted forward by 1 [E1,E2,E3]
    #   abc123->bbc123, level->mevely, Hello->Iello, Zebra->Aebra, Example->Fxample,
    #   test->uest, lazy->mazy, banana->canana, function->gunction, world->xorld,
    #   racecar->sacecar, aMiXeD->bMiXeD
    # All other characters (letters, digits, spaces, symbols) are unchanged [E1,E2,E3]
    #   "Hello World function lazy" -> "Iello World function lazy" [E1]
    #   "banana a data " -> "canana a data " [E3]
    #   "racecar Example racecar" -> "sacecar Example racecar" [E3]
    # 'z'/'Z' wraps to 'a'/'A' [E1: Zebra->Aebray]
    # A trailing 'y' is appended to every output [E1,E2,E3]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 1) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 1) % 26 + ord('A'))
        return c
    outs = []
    for s in probe.get("inputs", []):
        if s:
            outs.append(shift(s[0]) + s[1:] + "y")
        else:
            outs.append("y")
    return {"outputs": outs}

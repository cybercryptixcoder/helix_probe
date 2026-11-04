def predict(probe):
    # f reverses the string [E1: hello->olleh, abc->cba, x->x]
    # f inserts a capital W at the midpoint [E1: hello->olWleh (W after 2 chars),
    #   world->dlWrow (after 2), abc->cWba (after 1), x->Wx (after 0),
    #   test 123->321 Wtset (after 3), a b c->c Wb a (after 1),
    #   ABC->CWBA (after 1), the quick brown fox->xof nworbW kciuq eht (after 7),
    #   Hello World->dlroWW olleH (after 5), Hello, World!->!dlroWW ,olleH (after 5)]
    # Midpoint = len(s)//2, W inserted at that index of the reversed string.
    # "Hello World" has len 11, //2=5 -> dlroW|W olleH matches.
    # "Hello, World!" len 13, //2=6 -> !dlroW|W ,olleH matches.
    out = []
    for s in probe.get("inputs", []):
        r = s[::-1]
        m = len(s) // 2
        out.append(r[:m] + "W" + r[m:])
    return {"outputs": out}

def predict(probe):
    # f(x) = x + 1 for x >= 0 [E1: 0->-1? no; 1->2, 2->3, 4->5, 8->9, 16->17, 32->33, 64->65, 96->97, 128->129]
    # f(x) = x - 1 for x < 0 [E1: -1->-2, -2->-3, -4->-5, -8->-9, -16->-17, -32->-33, -64->-65, -96->-97, -128->-129]
    # At x = 0: observed -1, which matches x - 1, so the rule is x-1 for x <= 0 and x+1 for x > 0.
    # ? Boundary at 0 is the only special point; no other region seen.
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif x > 0:
            out.append(x + 1)
        else:
            out.append(x - 1)
    return {"y": out}

def predict(probe):
    # f(x) = x + 1 for x > 0 [E1: 1->2, 2->3, 4->5, 8->9, 16->17, 32->33, 64->65, 96->97, 128->129; E2: 0.1->1, 0.25->1, 0.5->1, 1.5->2, 2.5->3, 3->4]
    # f(x) = x - 1 for x <= 0 [E1: 0->-1, -1->-2, -2->-3, -4->-5, -8->-9, -16->-17, -32->-33, -64->-65, -96->-97, -128->-129; E2: -0.1->-2, -0.25->-2, -0.5->-2, -1.5->-3, -2.5->-4, -3->-4]
    # E2 shows the rule is NOT x±1 at fractional values; instead it looks like floor/ceil:
    #   x > 0: output = ceil(x) + 1? Check: 0.1->1, 0.25->1, 0.5->1, 1.5->2, 2.5->3, 3->4.
    #     ceil(0.1)+1=2 no. floor(x)+1: 0.1->1, 0.5->1, 1.5->2, 2.5->3, 3->4. Yes! floor(x)+1 for x>0.
    #     But E1 integers: 1->2=floor(1)+1, 2->3, 128->129. Consistent.
    #   x <= 0: floor(x)-1? -0.1->-2 (floor=-1, -1-1=-2 yes), -0.5->-2 (floor=-1 ->-2 yes),
    #     -1.5->-3 (floor=-2 ->-3 yes), -2.5->-4 (floor=-3 ->-4 yes), -3->-4 (floor=-3 ->-4 yes),
    #     0->-1 (floor=0 ->-1 yes), -128->-129 yes. Consistent!
    # So: f(x) = floor(x) + 1 for x > 0; f(x) = floor(x) - 1 for x <= 0.
    import math
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif x > 0:
            out.append(math.floor(x) + 1)
        else:
            out.append(math.floor(x) - 1)
    return {"y": out}

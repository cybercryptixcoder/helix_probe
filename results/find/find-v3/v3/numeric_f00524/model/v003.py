def predict(probe):
    # f(x) = round(x) when round(x) in {1,2,3,4} or {-1,-2,-3,-4}, else 0 [E1,E2]
    # Rounding is round-half-up: 0.5->1, 1.5->2, 2.5->3, 3.5->4 [E2]
    # E3: 1.2 -> 2, not 1. So rounding is NOT round-half-up for 1.2.
    #   Reconsider: 1.2->2, 2.9->3, 0.5->1, 1.5->2, 2.5->3, 3.5->4.
    #   ceil? ceil(1.2)=2 yes, ceil(2.9)=3 yes, ceil(0.5)=1 yes, ceil(1.5)=2 yes,
    #   ceil(2.5)=3 yes, ceil(3.5)=4 yes, ceil(1)=1, ceil(2)=2, ceil(3)=3, ceil(4)=4.
    #   Negatives: -1->-1, -2->-2, -3->-3, -4->-4, -5->0. ceil(-1)=-1 yes...
    #   But ceil(-0.5)=0, ceil(-1.5)=-1. Need -1.5->? unknown. ceil matches all ints.
    #   So f(x) = ceil(x) if ceil(x) in [-4,-1] or [1,4], else 0. [E1,E2,E3]
    import math
    out = []
    for x in probe["x"]:
        r = math.ceil(x)
        if (1 <= r <= 4) or (-4 <= r <= -1):
            out.append(float(r))
        else:
            out.append(0.0)
    return {"y": out}

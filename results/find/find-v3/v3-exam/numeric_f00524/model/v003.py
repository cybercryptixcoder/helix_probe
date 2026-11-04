def predict(probe):
    # f(x) = round-half-up(x) for |x| < 5, else 0 [E1, E2]
    #   - 4.0 -> 4, -4.0 -> -4, but 10.0 -> 0: active region is |x| < 5 [E2]
    #   - 2.5 -> 3, -2.5 -> -2: rounding is half-up (toward +inf on .5) [E2]
    #   - 0.4 -> 1, -0.4 -> -0.0: consistent with round-half-up [E2]
    #   - 2.9 -> 3, 3.1 -> 4, 3.4 -> 4: ordinary rounding [E1, E2]
    #   - large values (|x| >= 5) -> 0 [E1: 88.2, 66.0, -20.3, ... all 0]
    #   - 1.2 -> 2 [E3]: rounding is half-up, so 1.2 -> 1? No, observed 2.
    #     Recheck: 0.4->1, 1.5->2, 2.4->3, 2.5->3, 2.6->3, 2.9->3, 3.0->3,
    #     3.1->4, 3.4->4, 1.2->2. Pattern: floor(x)+1 for non-integers? 
    #     0.4->1=floor+1, 1.2->2=floor+1, 1.5->2=floor+1, 2.4->3=floor+1,
    #     2.5->3=floor+1, 2.6->3=floor+1, 2.9->3=floor+1, 3.1->4=floor+1,
    #     3.4->4=floor+1. Integers: 3.0->3, 0.0->0, 4.0->4, -4.0->-4.
    #     Negatives: -2.4->-2, -2.5->-2, -2.9->-2, -3.0->-3, -3.1->-3, -1.5->-1.
    #     -2.4: floor=-3, +1=-2 ✓. -2.5: floor=-3,+1=-2 ✓. -2.9: floor=-3,+1=-2 ✓.
    #     -3.1: floor=-4,+1=-3 ✓. -1.5: floor=-2,+1=-1 ✓. -0.4: floor=-1,+1=0 ✓.
    #     So: integers -> x, non-integers -> floor(x)+1 (i.e. ceil(x)).
    import math
    out = []
    for x in probe["x"]:
        if -5.0 < x < 5.0:
            if x == math.floor(x):
                out.append(float(x))
            else:
                out.append(float(math.floor(x) + 1))
        else:
            out.append(0.0)
    return {"y": out}

def predict(probe):
    # f(x) = round away from zero, then move 1 further away from zero [E1,E2,E3,E4]
    #   positive: ceil(x) + 1   [E1: 88.2->89, 66.0->67, 2.9->3, 21.3->22; E2: 0.5->1, 100->101; E4: 0.9->1, 1.1->2, 2.0->3, 50.5->51]
    #   negative: floor(x) - 1  [E1: -20.3->-22, -6.0->-7; E2: -0.5->-2, -100->-101; E4: -0.9->-2, -1.1->-3, -50.5->-52]
    #   zero: -1 (treated as non-positive) [E4: 0.0->-1]
    import math
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(float(math.ceil(x) + 1))
        else:
            out.append(float(math.floor(x) - 1))
    return {"y": out}

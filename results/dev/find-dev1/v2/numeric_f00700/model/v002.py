def predict(probe):
    # f(x) = ceil(x)+1 for x>0 [E1,E2: 0.01->2, 0.99->2, 1.01->3, 1.9->3, 2.01->4, 3.5->5]
    # f(x) = floor(x)-1 for x<=0 [E1,E2: 0->-1, -0.99->-1, -1.01->-2, -1.5->-2, -2.01->-3, -3.5->-4]
    import math
    out = []
    for x in probe["x"]:
        if x > 0:
            y = math.ceil(x) + 1
        else:
            y = math.floor(x) - 1
        out.append(y)
    return {"y": out}

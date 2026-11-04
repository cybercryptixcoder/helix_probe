def predict(probe):
    # f(x) = ceil(x)+1 for x>0 [E1,E2,E3]
    # f(x) = ceil(x)-1 for x<=0 [E1,E2,E3: 0->-1, -0.5->-1, -1->-2, -1.5->-2, -127.5->-128]
    import math
    out = []
    for x in probe["x"]:
        if x > 0:
            y = math.ceil(x) + 1
        else:
            y = math.ceil(x) - 1
        out.append(y)
    return {"y": out}

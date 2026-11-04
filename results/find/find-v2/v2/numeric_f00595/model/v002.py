def predict(probe):
    # f(x) = floor(x) + 1 for x >= 0, floor(x) - 1 for x < 0 [E1, E2]
    # At x=0: f(0) = -1, so 0 falls in the negative branch [E2]
    # Integer check: f(1)=2, f(2)=3, f(3)=4 (floor+1); f(-1)=-2, f(-2)=-3, f(-3)=-4 (floor-1) [E2]
    import math
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(math.floor(x) + 1)
        else:
            out.append(math.floor(x) - 1)
    return {"y": out}

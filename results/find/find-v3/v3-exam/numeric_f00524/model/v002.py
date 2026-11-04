def predict(probe):
    # f(x) = round-half-up(x) for |x| < 5, else 0 [E1, E2]
    #   - 4.0 -> 4, -4.0 -> -4, but 10.0 -> 0: active region is |x| < 5 [E2]
    #   - 2.5 -> 3, -2.5 -> -2: rounding is half-up (toward +inf on .5) [E2]
    #   - 0.4 -> 1, -0.4 -> -0.0: consistent with round-half-up [E2]
    #   - 2.9 -> 3, 3.1 -> 4, 3.4 -> 4: ordinary rounding [E1, E2]
    #   - large values (|x| >= 5) -> 0 [E1: 88.2, 66.0, -20.3, ... all 0]
    import math
    out = []
    for x in probe["x"]:
        if -5.0 < x < 5.0:
            out.append(float(math.floor(x + 0.5)))
        else:
            out.append(0.0)
    return {"y": out}

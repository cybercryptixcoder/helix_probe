def predict(probe):
    # f(x) = 1 for x in [-1.75, 1.75], else 0 [E1, E2, E3]
    # E3: 1 at -1.75 and 1.75, 0 at -2.0 and 2.0 -> boundary in (-2,-1.75] and [1.75,2)
    # E2: 1 at ±1.5, 0 at ±3 (consistent); E1: 1 at -1,0,1, 0 at ±2 (consistent)
    # Best guess: boundary at ±1.75 (last tested 1-point) ? 
    out = []
    for x in probe["x"]:
        if -1.75 <= x <= 1.75:
            out.append(1.0)
        else:
            out.append(0.0)
    return {"y": out}

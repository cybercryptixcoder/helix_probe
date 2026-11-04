def predict(probe):
    # Inside |x|<4: output ~12 (mean of E1,E2 inside values) [E1,E2]
    # Outside |x|<4: output ~0 (noise around 0) [E1,E2]
    # Boundary between 2.9 (high) and 5 (low); guess 4 [E1,E2]
    import math
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif abs(x) < 4:
            out.append(12.0)
        else:
            out.append(0.0)
    return {"y": out}

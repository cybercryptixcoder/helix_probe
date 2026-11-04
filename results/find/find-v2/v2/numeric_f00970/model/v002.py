def predict(probe):
    # Inside |x|<~3.5: output ~12 (mean of inside values) [E1,E2]
    # Outside |x|>~3.5: output ~0 (noise around 0) [E1,E2,E3]
    # Boundary between 2.9 (high) and 5 (low); guess 4 [E1,E2]
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif abs(x) < 4:
            out.append(12.0)
        else:
            out.append(0.0)
    return {"y": out}

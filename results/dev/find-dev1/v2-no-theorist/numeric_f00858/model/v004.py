def predict(probe):
    # f(x) = 1 for x in (-1.85, 1.85) roughly; 0 outside [E1, E2, E3, E4]
    # E4: 1 at ±1.85, 0 at ±1.9 -> boundary in (1.85, 1.9)
    # E3: 1 at ±1.75, 0 at ±2.0 (consistent)
    # E2: 1 at ±1.5, 0 at ±3 (consistent)
    # E1: 1 at ±1, 0 at ±2 (consistent)
    # Best guess: boundary at ±1.875 (midpoint of 1.85 and 1.9) ?
    out = []
    for x in probe["x"]:
        if -1.875 < x < 1.875:
            out.append(1.0)
        else:
            out.append(0.0)
    return {"y": out}

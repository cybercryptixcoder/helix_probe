def predict(probe):
    # f(x) = 1 on an interval around 0, 0 outside [E1]
    # Interval is symmetric about 0 [E2, E3, E4]
    # 1 at ±1.85, 0 at ±1.9 [E4]
    # 0 at ±1.86 and beyond [E5] -> boundary is below 1.86
    # 1 at ±1.8 [E4] -> boundary is above 1.8
    # Best guess: boundary at ±1.85 (1 at 1.85 from E4, 0 at 1.86 from E5) ?
    out = []
    for x in probe["x"]:
        if -1.85 <= x <= 1.85:
            out.append(1.0)
        else:
            out.append(0.0)
    return {"y": out}

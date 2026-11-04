def predict(probe):
    # Ramp region: y = 5.2 - 2.5*x on |x| <= 2.1 [E6, E8, E10, E12]
    # Outside: y ≈ 0 [E1, E3, E7, E9, E11]
    # Boundary inclusive at ±2.1 (E12: -2.1 ramp, -2.11 zero; 2.1 ramp, 2.11 zero)
    ys = []
    for x in probe["x"]:
        if x is None:
            ys.append(None)
            continue
        if -2.1 <= x <= 2.1:
            ys.append(5.2 - 2.5 * x)
        else:
            ys.append(0.0)
    return {"y": ys}

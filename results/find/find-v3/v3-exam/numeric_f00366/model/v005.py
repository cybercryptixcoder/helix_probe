def predict(probe):
    # Negative side, x < -4.25 -> 8.8 [E2, E5, E7]
    # Negative side, -4.25 <= x < 0 -> 9.8 [E6, E8: -4.0 is 9.8, -4.5 is 8.8]
    #   Boundary between -4.0 and -4.5; use -4.25
    # x == 0 -> 1548.92 [E2]
    # 0 < x < 4.25 -> -11.4 [E2, E4]
    # x >= 4.25 -> -12.4 [E4: 4.0 is -11.4, 4.5 is -12.4]
    out = []
    for x in probe["x"]:
        if x < -4.25:
            out.append(8.8)
        elif x < 0:
            out.append(9.8)
        elif x == 0:
            out.append(1548.92)
        elif x < 4.25:
            out.append(-11.4)
        else:
            out.append(-12.4)
    return {"y": out}

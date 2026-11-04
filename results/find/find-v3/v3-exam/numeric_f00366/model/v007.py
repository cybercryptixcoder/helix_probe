def predict(probe):
    # Negative side, x < -4.125 -> 8.8 [E12: -4.1 is 9.8, -4.15 is 8.8]
    # Negative side, -4.125 <= x < 0 -> 9.8 [E6, E12]
    # x == 0 -> 1548.92 [E2]
    # 0 < x < 4.15 -> -11.4 [E2, E4, E10: 4.1 is -11.4]
    # x >= 4.15 -> -12.4 [E10: 4.2 is -12.4]
    out = []
    for x in probe["x"]:
        if x < -4.125:
            out.append(8.8)
        elif x < 0:
            out.append(9.8)
        elif x == 0:
            out.append(1548.92)
        elif x < 4.15:
            out.append(-11.4)
        else:
            out.append(-12.4)
    return {"y": out}

def predict(probe):
    # Negative side:
    #   x < -4.11 -> 8.8 [E12: -4.15 is 8.8; E16: -4.12 is 8.8]
    #   -4.11 <= x < 0 -> 9.8 [E12: -4.1 is 9.8; E16: -4.08 is 9.8; E6, E14]
    # x == 0 -> 1548.92 [E2]
    # Positive side:
    #   0 < x < 4.14 -> -11.4 [E2, E14: 0.01 is -11.4]
    #   x >= 4.14 -> -12.4 [E14: 4.14 is -12.4; E10: 4.2 is -12.4]
    out = []
    for x in probe["x"]:
        if x < -4.11:
            out.append(8.8)
        elif x < 0:
            out.append(9.8)
        elif x == 0:
            out.append(1548.92)
        elif x < 4.14:
            out.append(-11.4)
        else:
            out.append(-12.4)
    return {"y": out}

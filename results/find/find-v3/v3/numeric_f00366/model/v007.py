def predict(probe):
    # x == 0 -> 1548.92 spike [E2]
    # -4.1 <= x < 0 -> 9.8 [E2,E4,E6,E9]
    # x < -4.1 -> 8.8 [E1,E4,E5,E7,E9,E11,E12]
    # 0 < x <= 4.1 -> -11.4 [E2,E4,E6,E10]
    # x > 4.1 -> -12.4 [E1,E3,E5,E7,E8,E10,E11,E12]
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(1548.92)
        elif x < 0:
            if x >= -4.1:
                out.append(9.8)
            else:
                out.append(8.8)
        else:  # x > 0
            if x <= 4.1:
                out.append(-11.4)
            else:
                out.append(-12.4)
    return {"y": out}

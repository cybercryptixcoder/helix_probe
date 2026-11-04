def predict(probe):
    # Piecewise step function of x, boundaries at -5, 0, 5 [E1,E2,E3,E4]
    # x < -5: 8.8 [E1,E2,E4]
    # -5 <= x < 0: 9.8 [E2,E4]  (boundary: -5.0 -> 8.8, -4.5 -> 8.8, -4.0 -> 9.8)
    # x = 0: 1548.92 spike [E2]
    # 0 < x < 5: -11.4 [E1,E2,E3,E4]
    # x >= 5: -12.4 [E1,E2,E3,E4]  (boundary: 4.5 -> -11.4, 5.0 -> -12.4)
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(1548.92)
        elif x < -4.5:
            out.append(8.8)
        elif x < 0:
            out.append(9.8)
        elif x < 5:
            out.append(-11.4)
        else:
            out.append(-12.4)
    return {"y": out}

def predict(probe):
    # Output is piecewise by sign of x [E1, E2]
    # x < -5: 8.8 [E1, E2]
    # -5 <= x < 0: 9.8 [E2]  (boundary at -5: -5.0 -> 8.8, -4.0 -> 9.8)
    # x = 0: 1548.92 [E2]
    # 0 < x < 5: -11.4 [E1, E2]  (5.0 -> -12.4, 4.0 -> -11.4)
    # x >= 5: -12.4 [E1, E2]
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(1548.92)
        elif x < -5:
            out.append(8.8)
        elif x < 0:
            out.append(9.8)
        elif x < 5:
            out.append(-11.4)
        else:
            out.append(-12.4)
    return {"y": out}

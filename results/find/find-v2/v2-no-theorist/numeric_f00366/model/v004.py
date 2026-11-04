def predict(probe):
    # Positive x: -11.4 for 0 < x < 4.11, -12.4 for x >= 4.11 [E2, E4, E8]
    #   E8: 4.09 -> -11.4; 4.11 -> -12.4; threshold between 4.09 and 4.11
    # Negative x: 9.8 for -4.11 < x < 0, 8.8 for x <= -4.11 [E2, E4, E8]
    #   E8: -4.09 -> 9.8; -4.11 -> 8.8
    # x == 0 is special: returns 1548.92 [E8]
    # x very small nonzero behaves like its sign [E8: 0.001->-11.4, -0.001->9.8]
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(1548.92)
        elif x > 0:
            out.append(-11.4 if x < 4.11 else -12.4)
        else:
            out.append(9.8 if -x < 4.11 else 8.8)
    return {"y": out}

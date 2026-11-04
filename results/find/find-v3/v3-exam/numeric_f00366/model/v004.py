def predict(probe):
    # Negative side: x < -1 -> 8.8 [E2: -30,-15,-5,-100]
    # x in [-1, 0) -> 9.8 [E2: -1,-0.5; E6: -1.5..-0.01 all 9.8]
    #   E6 shows 9.8 extends to at least -1.5; boundary between 8.8 and 9.8 is somewhere <= -1.5
    # x == 0 -> 1548.92 [E2]
    # 0 < x < 4 -> -11.4 [E2: 0.5,1,3; E4: 0.01..2]
    # x >= 4 -> -12.4 [E4: 4.0 is -11.4, 4.5+ is -12.4; E2: 5+]
    #   So transition is between 4.0 and 4.5
    out = []
    for x in probe["x"]:
        if x < -1.5:
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

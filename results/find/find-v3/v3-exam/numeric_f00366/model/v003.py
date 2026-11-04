def predict(probe):
    # Negative x -> 8.8 [E1, E2]
    # x == 0 -> 1548.92 [E2]
    # 0 < x < 4 -> -11.4 [E2: 0.5,1,3; E4: 0.01,0.1,0.9,1,2]
    # 4 <= x -> -12.4 [E4: 4.5,4.9,5,5.1; E2: 5,7,8,9,10,...]
    # x in (-1,0) -> 9.8 [E2: -0.5]; x == -1 -> 9.8 [E2]
    # So: x <= -1 -> 8.8 ; -1 < x < 0 -> 9.8 ; x == 0 -> 1548.92
    #     0 < x < 4 -> -11.4 ; x >= 4 -> -12.4
    out = []
    for x in probe["x"]:
        if x <= -1:
            out.append(8.8)
        elif x < 0:
            out.append(9.8)
        elif x == 0:
            out.append(1548.92)
        elif x < 4:
            out.append(-11.4)
        else:
            out.append(-12.4)
    return {"y": out}

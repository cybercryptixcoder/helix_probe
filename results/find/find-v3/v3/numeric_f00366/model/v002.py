def predict(probe):
    # Outputs are piecewise constant [E1, E2]
    # x < 0: 8.8, except near zero where it's 9.8 [E2]
    # x = 0: 1548.92 [E2]
    # 0 < x < ~5: -11.4 [E1, E2]
    # x >= ~5 (positive): -12.4 [E1, E2]
    # Negative side: -5 and below -> 8.8; -3,-1,-0.5,-0.1 -> 9.8 [E2]
    # So there's a band around 0 on the negative side giving 9.8.
    # Boundary between 9.8 and 8.8 on negative side is between -3 and -5 [E2]
    # Boundary between -11.4 and -12.4 on positive side is between 3 and 5 [E2]
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif x == 0:
            out.append(1548.92)
        elif x < 0:
            if x > -4:  # ? boundary between -3 and -5
                out.append(9.8)
            else:
                out.append(8.8)
        else:  # x > 0
            if x < 4:  # ? boundary between 3 and 5
                out.append(-11.4)
            else:
                out.append(-12.4)
    return {"y": out}

def predict(probe):
    # Piecewise constant function of x.
    # Negative side: 8.8 for x <= -4.1, 9.8 for -3.9 <= x < 0 [E2, E4]
    #   boundary between -4.1 and -3.9 -> use -4.0
    # x = 0: 1548.92 (spike) [E2]
    # Positive side: -11.4 for 0 < x <= 4.1, -12.4 for x >= 4.5 [E2, E4]
    #   boundary between 4.1 and 4.5 -> use 4.3
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif x == 0:
            out.append(1548.92)
        elif x < 0:
            out.append(9.8 if x > -4.0 else 8.8)
        else:  # x > 0
            out.append(-11.4 if x < 4.3 else -12.4)
    return {"y": out}

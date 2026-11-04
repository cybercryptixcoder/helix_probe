def predict(probe):
    # Piecewise constant with sign-based regions.
    # Negative side: 8.8 for x <= -4.0, 9.8 for -4.0 < x < 0 [E4, E8]
    #   E8: -4.05 -> 9.8, -4.0 -> 9.8, -3.95 -> 9.8
    #   E4: -4.1 -> 9.8, -4.5 -> 8.8, -4.9 -> 8.8
    #   So boundary is between -4.5 and -4.1; use -4.3 (midpoint-ish)
    # Positive side: -11.4 for 0 < x < 4.2, -12.4 for x >= 4.2 [E4, E8]
    #   E8: 4.15 -> -12.4, 4.2 -> -12.4, 4.25 -> -12.4
    #   E4: 4.1 -> -11.4, 4.5 -> -12.4
    #   So boundary is between 4.1 and 4.15; use 4.125
    # x = 0: 1548.92 (spike) [E2]
    # Narrow band around 0 does NOT return spike; sign rule applies [E6]
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif x == 0:
            out.append(1548.92)
        elif x < 0:
            out.append(9.8 if x > -4.3 else 8.8)
        else:  # x > 0
            out.append(-11.4 if x < 4.125 else -12.4)
    return {"y": out}

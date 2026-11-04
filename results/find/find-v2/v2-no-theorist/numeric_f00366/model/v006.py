def predict(probe):
    # Positive x: -11.4 for 0 < x < 4.1, -12.4 for x >= 4.1 [E4, E8, E12, E14, E16]
    #   E16: 4.1 -> -11.4; 4.1001 -> -12.4; 4.099 -> -11.4; 4.095 -> -11.4
    #   E14: 4.0999 -> -11.4; 4.101 -> -12.4
    #   => threshold between 4.1 and 4.1001 (so ~4.1, inclusive at 4.1)
    # Negative x: 9.8 for -4.1 < x < 0, 8.8 for x <= -4.1 [E4, E8, E12, E14, E16]
    #   E16: -4.1 -> 9.8; -4.1001 -> 8.8; -4.099 -> 9.8; -4.095 -> 9.8
    #   E14: -4.0999 -> 9.8; -4.101 -> 8.8
    #   => threshold between -4.1 and -4.1001 (so ~-4.1, inclusive at -4.1)
    # x == 0 is special: returns 1548.92 [E8]
    # x very small nonzero behaves like its sign [E8: 0.001->-11.4, -0.001->9.8]
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(1548.92)
        elif x > 0:
            out.append(-11.4 if x <= 4.1 else -12.4)
        else:
            out.append(9.8 if -x <= 4.1 else 8.8)
    return {"y": out}

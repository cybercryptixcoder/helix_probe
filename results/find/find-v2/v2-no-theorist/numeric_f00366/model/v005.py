def predict(probe):
    # Positive x: -11.4 for 0 < x < 4.105, -12.4 for x >= 4.105 [E2, E4, E8, E12, E14]
    #   E14: 4.0999 -> -11.4; 4.101 -> -12.4; 4.105 -> -12.4; 4.109 -> -12.4
    #   E12: 4.095 -> -11.4; 4.105 -> -12.4
    #   => threshold between 4.0999 and 4.101 (so ~4.10)
    # Negative x: 9.8 for -4.105 < x < 0, 8.8 for x <= -4.105 [E2, E4, E8, E12, E14]
    #   E14: -4.0999 -> 9.8; -4.101 -> 8.8; -4.105 -> 8.8
    #   E12: -4.095 -> 9.8; -4.105 -> 8.8
    #   => threshold between -4.0999 and -4.101 (so ~-4.10)
    # x == 0 is special: returns 1548.92 [E8]
    # x very small nonzero behaves like its sign [E8: 0.001->-11.4, -0.001->9.8]
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(1548.92)
        elif x > 0:
            out.append(-11.4 if x < 4.10 else -12.4)
        else:
            out.append(9.8 if -x < 4.10 else 8.8)
    return {"y": out}

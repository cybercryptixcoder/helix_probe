def predict(probe):
    # Output takes only four values: -12.4, 8.8, -11.4, 9.8 [E1-E10]
    # x > ~3 -> -12.4 [E1: 21.3; E2: 30.3; E6-E10 all large positives]
    # 0 < x <= ~3 -> -11.4 [E1: 2.9; E2: 1.2; E6: 2.0]
    # x < 0 -> 8.8 generally [E1: -20.3; E4: -5.9; E6-E9]
    # small negative region gives 9.8: -3.5 and -1.6 inside [E5, E10]
    #   -5.9 is outside (8.8) [E4]; so boundary is between -5.9 and -3.5
    #   ? upper boundary: -1.6 inside, 0 not tested; assume x<0 region
    #   ? lower boundary: pick -4.0 as guess between -5.9 and -3.5
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif x > 0:
            if x <= 2.9:
                out.append(-11.4)
            else:
                out.append(-12.4)
        else:
            if -4.0 <= x < 0:
                out.append(9.8)
            else:
                out.append(8.8)
    return {"y": out}

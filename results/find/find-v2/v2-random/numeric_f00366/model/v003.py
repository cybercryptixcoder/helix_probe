def predict(probe):
    # Output takes only three values: -12.4, 8.8, -11.4, and 9.8 [E1-E5]
    # x > ~3 -> -12.4 [E1: 2.9->-11.4, 21.3->-12.4; E2: 30.3->-12.4]
    # 0 < x < ~3 -> -11.4 [E1: 2.9; E2: 1.2]
    # x < 0 -> 8.8, except a small negative region gives 9.8 [E5: -1.6->9.8]
    # ? Boundary of small-negative region unknown; -1.6 is inside, -5.9 outside [E4]
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
            if -2.0 <= x < 0:
                out.append(9.8)
            else:
                out.append(8.8)
    return {"y": out}

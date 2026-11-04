def predict(probe):
    # x=0 gives special value 1548.92 [E2, E18]
    # |x| < ~4.12: small magnitude (9.8 for x<0, -11.4 for x>0) [E4,E8,E12,E14,E16]
    # |x| > ~4.12: large magnitude (8.8 for x<0, -12.4 for x>0) [E1,E3,E5,E7,E9,...]
    B = 4.12  # boundary (?) between -4.12 and -4.1, and 4.1 and 4.14
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(1548.92)
        elif x < 0:
            out.append(9.8 if x > -B else 8.8)
        else:
            out.append(-11.4 if x < B else -12.4)
    return {"y": out}

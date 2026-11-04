def predict(probe):
    # x=0 gives special value 1548.92 [E2, E18]
    # |x| < ~4.1: 9.8 for x<0, -11.4 for x>0 [E4,E8,E12,E14,E16]
    # |x| > ~4.1: 8.8 for x<0, -12.4 for x>0 [E1,E3,E5,E7,E9,...]
    # Negative-side step 9.8->8.8 occurs between -4.1 and -4.105 [E22]
    # Positive-side step -11.4->-12.4 occurs between 4.1 and 4.13 [E10,E14,E20]
    BN = -4.1025  # negative boundary: x > BN -> 9.8, else 8.8
    BP = 4.11     # positive boundary: x < BP -> -11.4, else -12.4
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(1548.92)
        elif x < 0:
            out.append(9.8 if x > BN else 8.8)
        else:
            out.append(-11.4 if x < BP else -12.4)
    return {"y": out}

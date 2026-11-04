def predict(probe):
    # Sign-based step function with a near-zero band.
    # x < 0: 9.8 for -4 <= x < 0; 8.8 for x <= -4 [E4, E6]
    # x > 0: -11.4 for 0 < x <= 4; -12.4 for x > 4 [E4, E6]
    # x = 0: 1548.92 [E2]
    # Band edges: negative side between -4.5 and -4.0 [E6]; positive side between 4.0 and 4.5 [E6]
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(1548.92)
        elif x < 0:
            out.append(9.8 if x > -4.0 else 8.8)
        else:
            out.append(-11.4 if x < 4.0 else -12.4)
    return {"y": out}

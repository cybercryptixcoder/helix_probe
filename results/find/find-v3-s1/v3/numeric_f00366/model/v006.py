def predict(probe):
    # Sign-based step function with a near-zero band.
    # x < 0: 9.8 for -4.05 < x < 0; 8.8 for x <= -4.05 [E6, E8, E12]
    # x > 0: -11.4 for 0 < x <= 4.1; -12.4 for x > 4.1 [E4, E6, E8, E10]
    # x = 0: 1548.92 [E2]
    # Negative band edge between -4.1 and -4.05 [E12]
    # Positive band edge between 4.1 and 4.15 [E10]
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(1548.92)
        elif x < 0:
            out.append(9.8 if x > -4.05 else 8.8)
        else:
            out.append(-11.4 if x <= 4.1 else -12.4)
    return {"y": out}

def predict(probe):
    # Outputs are piecewise constant in sign of x, with a small band near zero [E1, E2]
    # x < 0: 8.8, except near zero (-0.5..-0.01) where it's 9.8 [E1, E2]
    # x > 0: -12.4, except near zero (0.01..0.5) where it's -11.4 [E2]
    # x = 0: huge value 1548.92 [E2]
    # Boundaries of the near-zero band are somewhere between 0.5 and 12.9 / 38.8 [?]
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(1548.92)
        elif x < 0:
            out.append(9.8 if x > -0.5 else 8.8)
        else:
            out.append(-11.4 if x < 0.5 else -12.4)
    return {"y": out}

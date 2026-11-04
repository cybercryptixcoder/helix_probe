def predict(probe):
    # Output is 52.2 for x > 0, -14.96 for x < 0 [E1, E2, E3, E4]
    # At x == 0, output is 898156.8 (a special value) [E4]
    # No other interval/region behavior observed; sign rule holds down to 1e-6 [E4]
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(52.2)
        elif x < 0:
            out.append(-14.96)
        else:
            out.append(898156.8)
    return {"y": out}

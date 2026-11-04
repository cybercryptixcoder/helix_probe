def predict(probe):
    # f(x) = 8 - 9.6*x for x > -9.5 [E1,E2,E3,E4,E5,E6]
    # f(x) ≈ 8 (noisy) for x <= -9.5 [E1,E2,E3,E5,E6]
    # boundary between -9.5 (special) and -9 (linear) [E6]
    out = []
    for x in probe["x"]:
        if x <= -9.5:
            out.append(8.0)
        else:
            out.append(8.0 - 9.6 * x)
    return {"y": out}

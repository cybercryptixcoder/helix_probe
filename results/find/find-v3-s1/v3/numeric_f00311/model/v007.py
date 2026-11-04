def predict(probe):
    # f(x) = 8 - 9.6*x for x > -9.4 [E6,E8,E10]
    # f(x) ≈ 8 (noisy) for x <= -9.4 [E6,E8,E10]
    # transition between -9.35 (linear, y=97.76) and -9.42 (flat) [E10]
    # boundary at -9.4: -9.35 linear, -9.42 flat [E10]
    out = []
    for x in probe["x"]:
        if x <= -9.4:
            out.append(8.0)
        else:
            out.append(8.0 - 9.6 * x)
    return {"y": out}

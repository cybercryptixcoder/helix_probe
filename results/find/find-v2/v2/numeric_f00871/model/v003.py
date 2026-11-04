def predict(probe):
    # f(x) = 5.2 - 2.5*x on the interval [-2.1, 2.08], else 0 [E2, E4]
    # Negative boundary: -2.1 gives 10.45, -2.2 gives 0 -> cutoff in (-2.2, -2.1], use -2.1 [E4]
    # Positive boundary: 2.08 gives 0.0, 2.04 gives 0.1 -> cutoff in (2.04, 2.08], use 2.08 [E4]
    # Inside interval, values follow 5.2-2.5x even where negative (2.1 -> -0.05) [E4]
    out = []
    for x in probe["x"]:
        if -2.1 <= x <= 2.08:
            out.append(5.2 - 2.5 * x)
        else:
            out.append(0.0)
    return {"y": out}

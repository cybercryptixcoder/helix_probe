def predict(probe):
    # f(x) = 5.2 - 2.5*x for x in [-2.1, 2.1], else 0 [E4, E8]
    # E8: x=-2.1 -> 10.45 (linear), x=-2.101 -> 0; x=2.1 -> -0.05 (linear), x=2.101 -> 0.
    #     So the region is exactly [-2.1, 2.1] inclusive.
    # Outside: 0 [E2, E5, E7]
    out = []
    for x in probe["x"]:
        if -2.1 <= x <= 2.1:
            out.append(5.2 - 2.5 * x)
        else:
            out.append(0.0)
    return {"y": out}

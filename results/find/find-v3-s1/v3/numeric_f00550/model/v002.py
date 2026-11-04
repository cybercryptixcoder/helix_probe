def predict(probe):
    # f(x) = 0 almost everywhere [E1, E2]
    # Nonzero only at x=0 -> -1.7, x=0.5 -> -1.625, x=-0.5 -> -3.425 [E2]
    # These look like isolated special points, not a region; model them as
    # exact-value exceptions. Everything else returns -0.0. [?]
    specials = {0.0: -1.7, 0.5: -1.625, -0.5: -3.425}
    out = []
    for x in probe["x"]:
        key = float(x)
        out.append(specials.get(key, -0.0))
    return {"y": out}

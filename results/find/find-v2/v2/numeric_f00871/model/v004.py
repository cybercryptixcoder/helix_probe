def predict(probe):
    # f(x) = 5.2 - 2.5*x on [-2.1, 2.08], else 0 [E2, E4, E6, E8]
    # Boundaries sharp: -2.1 included, -2.1001 excluded; 2.08 excluded, 2.0799 included [E6, E8]
    # Outside interval, output is 0 (signed zero possible) [E5, E7]
    # EXCEPTION: x=-79.1 gives 0.1766, not 0 [E9]
    #   -79.1 is outside [-2.1,2.08], so there is a second nonzero region near -79.1
    #   Value 0.1766 at x=-79.1; unknown shape/width of this region (?)
    #   Guess: a small bump/interval around -79.1; model as isolated point for now (?)
    out = []
    for x in probe["x"]:
        if -2.1 <= x <= 2.08:
            out.append(5.2 - 2.5 * x)
        elif abs(x + 79.1) < 0.05:
            out.append(0.1766)
        else:
            out.append(0.0)
    return {"y": out}

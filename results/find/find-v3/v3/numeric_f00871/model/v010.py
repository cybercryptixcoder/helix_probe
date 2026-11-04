def predict(probe):
    # f(x) = 5.2 - 2.5*x for x in [-2.1, 2.1], else 0 [E4, E8]
    # Outside that region: 0 [E2, E5, E7, E11, E13]
    # E9-E14: near x=-79.1 there is a noisy band with values ~0.0-0.32,
    #   no clear linear trend, spanning roughly [-79.9, -78.2].
    #   Best model: a noisy region; predict its mean ~0.13.
    out = []
    for x in probe["x"]:
        if -2.1 <= x <= 2.1:
            out.append(5.2 - 2.5 * x)
        elif -79.9 <= x <= -78.2:
            # ? noisy second region near x=-79.1; mean ~0.13, no clear slope
            out.append(0.13)
        else:
            out.append(0.0)
    return {"y": out}

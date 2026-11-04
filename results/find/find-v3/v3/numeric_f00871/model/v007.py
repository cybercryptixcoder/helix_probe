def predict(probe):
    # f(x) = 5.2 - 2.5*x for x in [-2.1, 2.1], else 0 [E4, E8]
    # E8: x=-2.1 -> 10.45 (linear), x=-2.101 -> 0; x=2.1 -> -0.05 (linear), x=2.101 -> 0.
    #     So the region is exactly [-2.1, 2.1] inclusive.
    # Outside: 0 [E2, E5, E7]
    # E9: x=-79.1 -> 0.1155 (nonzero!). This is a second small linear region.
    #     Need to find its extent. 0.1155 = 5.2 - 2.5*x => x = 2.034? No.
    #     Try: 0.1155 could be from a different line. Let's hypothesize a second
    #     region around x=-79.1. Without more data, guess a small linear region.
    # ? Second region near x=-79.1 with value 0.1155. Unknown slope/extent.
    out = []
    for x in probe["x"]:
        if -2.1 <= x <= 2.1:
            out.append(5.2 - 2.5 * x)
        elif -79.2 <= x <= -79.0:
            # ? guess: linear passing through (-79.1, 0.1155); slope unknown, assume 0
            out.append(0.1155)
        else:
            out.append(0.0)
    return {"y": out}

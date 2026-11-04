def predict(probe):
    # f(x) = 5.2 - 2.5*x for x in [-2.1, 2.1], else 0 [E4, E8]
    # Outside that region: 0 [E2, E5, E7]
    # E9: x=-79.1 -> 0.1155 (nonzero). E10 shows a noisy band around x=-79.1
    #     with values ~0.01-0.25, no clear linear trend -> treat as noise.
    #     Best guess: the box adds small noise near x=-79.1 (a second active
    #     region), but the values are noisy so we can't pin a formula.
    #     Model it as a small noisy region; predict its mean ~0.11.
    out = []
    for x in probe["x"]:
        if -2.1 <= x <= 2.1:
            out.append(5.2 - 2.5 * x)
        elif -79.3 <= x <= -78.8:
            # ? noisy second region near x=-79.1; mean ~0.11, no clear slope
            out.append(0.11)
        else:
            out.append(0.0)
    return {"y": out}

def predict(probe):
    # f(x) = ceil(x) on a band, else 0 [E2, E4]
    # Positive side: ceil applies for x <= 4, but NOT for x >= 4.1 [E4, E6]
    #   x=4 -> 4, x=4.1 -> 5 (!), x=4.5 -> 0 [E4, E6]
    # Negative side: ceil applies for x >= -4, NOT for x <= -4.1 [E4, E6]
    #   x=-4 -> -4, x=-4.1 -> -4 (!), x=-4.5 -> 0 [E4, E6]
    # So band is [-4, 4] for the ceil rule, but the boundary is fuzzy:
    #   just past 4 (4.1) still gives ceil=5, then drops to 0 by 4.5
    #   just past -4 (-4.1) still gives ceil=-4, then drops to 0 by -4.5
    # Model: ceil applies on [-4.1, 4.1]? but 4.5->0, -4.5->0, 4.1->5, -4.1->-4
    # Best guess: band is (-4.5, 4.5) but with ceil, and 4.1->5 means ceil(4.1)=5
    #   Actually ceil(4.1)=5, ceil(-4.1)=-4. So ceil applies on (-4.5, 4.5)!
    #   Check: 4.5 -> 0 (boundary excluded), 4.1 -> 5 (ceil(4.1)=5) [E6]
    #   Check: -4.5 -> 0, -4.1 -> -4 (ceil(-4.1)=-4) [E6]
    #   Check: 4 -> 4, -4 -> -4 [E4]; 5 -> 0, -5 -> 0 [E4]
    # So: ceil(x) if -4.5 < x < 4.5, else 0
    import math
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif -4.5 < x < 4.5:
            out.append(float(math.ceil(x)))
        else:
            out.append(0.0)
    return {"y": out}

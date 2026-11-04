def predict(probe):
    # f is a small MLP approximating a piecewise-linear function.
    # For x >= ~-0.75: y = 111.43*x + 106.05  [E2, E4, E5, E7]
    # For x <= ~-1.5:  y = -26.07*x - 25.43  [E2, E4, E5, E7]
    # Between -1.5 and -0.75 there's a smooth dip (MLP blend), min ~6.42 at x~-1.05 [E4,E6,E8]
    # The dip is a rounded valley: rises on both sides toward the two lines.
    # Model the transition as a smooth blend between the two lines plus a
    # Gaussian-like bump that lifts the valley floor to ~6.42 at x=-1.05.
    import math
    out = []
    for x in probe["x"]:
        pos = 111.43 * x + 106.05
        neg = -26.07 * x - 25.43
        # smooth blend weight: 0 on neg side (x<-1.5), 1 on pos side (x>-0.75)
        t = (x + 1.5) / 0.75
        if t <= 0:
            w = 0.0
        elif t >= 1:
            w = 1.0
        else:
            w = t * t * (3 - 2 * t)  # smoothstep
        base = neg * (1 - w) + pos * w
        # valley correction: push up toward 6.42 near x=-1.05
        # observed dip floor ~6.42 at -1.05; base there ~ -26.07*-1.05-25.43=1.94
        # add a bump centered at -1.05
        bump = 4.5 * math.exp(-((x + 1.05) ** 2) / (2 * 0.18 ** 2))
        y = base + bump
        out.append(y)
    return {"y": out}

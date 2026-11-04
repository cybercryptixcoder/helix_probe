def predict(probe):
    # f is a small MLP approximating a piecewise-linear function.
    # For x >= ~-0.75: y = 111.43*x + 106.05  [E2, E4, E5, E7, E9]
    # For x <= ~-1.5:  y = -26.07*x - 25.43  [E2, E4, E5, E7, E10]
    # Between -1.5 and -0.75 the curve dips to a rounded valley floor
    #   ~6.37 at x~-1.06, rising smoothly to meet both lines [E4,E6,E8,E10].
    # The dip is asymmetric: the left side (from -1.5) falls steeply, the
    #   right side rises more gently toward the positive line.
    # Model: blend the two lines with a smoothstep, then add a bump so the
    #   valley floor matches ~6.37 at x=-1.06.
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
            w = t * t * (3 - 2 * t)
        base = neg * (1 - w) + pos * w
        # valley correction: base at -1.06 is ~1.9; observed floor ~6.37
        bump = 4.5 * math.exp(-((x + 1.06) ** 2) / (2 * 0.20 ** 2))
        y = base + bump
        out.append(y)
    return {"y": out}

def predict(probe):
    # Piecewise linear with common intercept 11.2, kink at x=0 [E1]
    # x >= 0: y = -22.5*x + 11.2 [E1]
    # x < 0:  y = -10.89*x + 11.2 [E1]
    out = []
    for x in probe["x"]:
        if x >= 0:
            out.append(-22.5 * x + 11.2)
        else:
            out.append(-10.89 * x + 11.2)
    return {"y": out}

def predict(probe):
    # Piecewise linear [E1]: for x>0, y = 16.4*x - 2.5; for x<0, y = -8.2*x + 2.5
    # Boundary at x=0 (unseen exactly; ?) [E1]
    # Slope ratio 2:1 between positive and negative branches [E1]
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(16.4 * x - 2.5)
        elif x < 0:
            out.append(-8.2 * x + 2.5)
        else:
            out.append(-2.5)  # ? x=0 unobserved
    return {"y": out}

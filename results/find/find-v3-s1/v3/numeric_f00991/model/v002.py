def predict(probe):
    # A: for x>0, y = 16.4*x - 2.5  [E1, E2]
    # B: for x<0, y = -8.2*x + 2.5  [E1, E2]
    # C: at x=0, y = 2.5 (matches negative branch limit, not positive)  [E2]
    # D: boundary at x=0; both branches meet near y=2.5 at 0  [E2]
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(16.4 * x - 2.5)
        else:
            out.append(-8.2 * x + 2.5)
    return {"y": out}

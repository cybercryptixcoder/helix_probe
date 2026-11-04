def predict(probe):
    # f(x) = 16.4x - 2.5 for x > 0 [E1, E2]
    # f(x) = -8.2x + 2.5 for x < 0 [E1, E2]
    # f(0) = 2.5 (uses the x<0 branch / or a special value) [E2]
    # Note: at x=0 observed 2.5, which matches the x<0 formula, not the x>0 formula.
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(16.4 * x - 2.5)
        else:
            out.append(-8.2 * x + 2.5)
    return {"y": out}

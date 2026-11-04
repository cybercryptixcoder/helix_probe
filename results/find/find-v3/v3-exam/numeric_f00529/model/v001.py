def predict(probe):
    # y is -6.9 for positive x, -7.9 for negative x [E1]
    # x=2.9 gives -6.9015, a tiny perturbation near zero [E1]
    # Hypothesis: y = -6.9 - 1.0*(x<0), with a small correction near x~0
    # The 2.9 case suggests something like -6.9 - 0.0015 at small positive x
    # Simplest guess: sign-based step, with a small dip for small |x|
    out = []
    for x in probe["x"]:
        if x < 0:
            out.append(-7.9)
        elif abs(x) < 3:
            out.append(-6.9015)
        else:
            out.append(-6.9)
    return {"y": out}

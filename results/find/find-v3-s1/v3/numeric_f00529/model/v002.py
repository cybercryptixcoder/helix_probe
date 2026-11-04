def predict(probe):
    # Outputs are only -7.9 or -6.9 (plus transitional values near 0) [E1, E2]
    # x <= 0 -> -7.9 [E1, E2]
    # x >= 5 -> -6.9 [E2]
    # Small positive x (0 < x < 5) gives intermediate values between -7.9 and -6.9 [E2]
    #   e.g. x=0.5 -> -7.8906, x=1 -> -7.8111, x=2 -> -6.9889 [E2]
    # Hypothesis: smooth transition from -7.9 to -6.9 over roughly 0 < x < 3 [E2, ?]
    #   Model as a logistic/smoothstep between -7.9 and -6.9.
    import math
    out = []
    for x in probe["x"]:
        if x <= 0:
            out.append(-7.9)
        elif x >= 5:
            out.append(-6.9)
        else:
            # smooth transition; fit roughly to E2 points
            # x=0.5 -> -7.8906, x=1 -> -7.8111, x=2 -> -6.9889
            # use logistic: -6.9 - 1.0/(1+exp(k*(x-c)))
            # Solve roughly: at x=2 nearly -6.9, at x=0.5 nearly -7.9
            # try c=1.0, k=2.0
            v = -6.9 - 1.0/(1.0 + math.exp(2.0*(x - 1.0)))
            out.append(v)
    return {"y": out}

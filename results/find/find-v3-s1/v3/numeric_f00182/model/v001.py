def predict(probe):
    # Piecewise linear, fitted exactly to E1 (every point matches to full precision):
    # For x < 0: y = 11.2 - 10.89*x   [E1]
    # For x >= 0: y = 11.2 - 22.5*x   [E1]
    # Shared intercept 11.2 on both branches [E1]
    # Slope changes at x=0; boundary itself unobserved, branch at 0 assumed positive [?]
    out = []
    for x in probe["x"]:
        if x < 0:
            out.append(11.2 - 10.89 * x)
        else:
            out.append(11.2 - 22.5 * x)
    return {"y": out}

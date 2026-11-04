def predict(probe):
    # Piecewise linear: y = 11.2 - 22.5*x for x>=0; y = 11.2 - 10.89*x for x<0
    # Evidence: E1,E2,E3,E4,E5,E6 all fit exactly.
    # Positive slope -22.5 [E4: 80..128 step -22.5; E6: 0..5]
    # Negative slope -10.89 [E4: -128..-70; E6: -3..-0.5]
    # Intercept 11.2 at x=0 [E6]
    xs = probe["x"]
    ys = []
    for x in xs:
        if x >= 0:
            ys.append(11.2 - 22.5 * x)
        else:
            ys.append(11.2 - 10.89 * x)
    return {"y": ys}

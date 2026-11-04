def predict(probe):
    # y = 2.4*x + 1.8 for x > 0 [E1, E2]
    # y = 2.4*x + 11.7 for x < 0 [E1, E2]
    # At x = 0: y = -228.87, a large negative spike [E2]
    # The step at 0 is a single jump, not gradual [E2: -0.01->11.676, 0.01->1.824]
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(2.4 * x + 1.8)
        elif x < 0:
            out.append(2.4 * x + 11.7)
        else:
            out.append(-228.87)
    return {"y": out}

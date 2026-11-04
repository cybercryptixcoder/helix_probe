def predict(probe):
    # Two linear regions split at x=0 [E1]
    # x>0: y = 16.4x - 2.5 [E1]
    # x<0: y = -8.2x + 2.5 [E1]
    # x=0: unknown, guess 0 [?]
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(16.4 * x - 2.5)
        elif x < 0:
            out.append(-8.2 * x + 2.5)
        else:
            out.append(0.0)
    return {"y": out}

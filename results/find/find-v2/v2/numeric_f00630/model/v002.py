def predict(probe):
    # Output is one of two constants: 52.2 or -14.96 [E1, E2]
    # Rule: y = 52.2 when x > 0, else -14.96 [E1, E2]
    # Exception: at x == 0 exactly, y = 898156.8 [E2]
    #   (x=0.0 -> 898156.8; x=0.001 -> 52.2; x=-0.001 -> -14.96)
    # Boundary at 0 confirmed: sign-based step, with a spike at exactly 0 [?]
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(898156.8)
        elif x > 0:
            out.append(52.2)
        else:
            out.append(-14.96)
    return {"y": out}

def predict(probe):
    # f(x) = round(x) when x is in a narrow band near 2-3, else 0 [E1, E2]
    # E1: x=2.9 -> 3.0; E2: x=1.2 -> 2.0. So band includes 1.2 and 2.9.
    # Other tested values (including 21.3, 30.3, -6.0) give 0.
    # Hypothesis (?): f(x) = round(x) for 1 <= x < 3, else 0.
    out = []
    for x in probe["x"]:
        if 1.0 <= x < 3.0:
            out.append(float(round(x)))
        else:
            out.append(0.0)
    return {"y": out}

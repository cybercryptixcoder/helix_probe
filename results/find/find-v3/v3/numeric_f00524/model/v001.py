def predict(probe):
    # Only one data point: f(2.9) = 3.0, everything else ~0 [E1]
    # Hypothesis: f(x) = round(x) for x in some small interval around 3, else 0?
    # Or f(x) = 3 only at x=2.9? Too little data to know the mechanism.
    # Best guess: output 3 when x rounds to 3 (i.e. 2.5 <= x < 3.5), else 0.
    # ? This is a guess; boundaries unknown.
    out = []
    for x in probe["x"]:
        if 2.5 <= x < 3.5:
            out.append(3.0)
        else:
            out.append(0.0)
    return {"y": out}

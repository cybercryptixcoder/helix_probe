def predict(probe):
    # f(x) is ~25 almost everywhere, with a small bump to 26 near x≈3 [E1]
    # All 10 probes gave 25 except x=2.9 gave 26 [E1]
    # Hypothesis: f(x) = 25 + 1 if x is in a small interval around 3, else 25
    # Boundaries unknown; guess a narrow interval around 3 (?)
    out = []
    for x in probe["x"]:
        if 2.0 <= x <= 4.0:
            out.append(26.0)
        else:
            out.append(25.0)
    return {"y": out}

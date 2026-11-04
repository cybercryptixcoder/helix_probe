def predict(probe):
    # f(x) is ~constant 25, with a rare 26 near x≈2.9 [E1]
    # Only one experiment; most values give 25.0, one gives 26.0
    # Hypothesis (?): output is 25 generally; 26 in a narrow region near x≈3
    out = []
    for x in probe["x"]:
        if 2.0 <= x <= 4.0:
            out.append(26.0)
        else:
            out.append(25.0)
    return {"y": out}

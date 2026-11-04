def predict(probe):
    # Outputs are only ever +18 or -18 [E1].
    # Sign pattern vs x in E1:
    #   x=-93.6 -> +18, x=88.9 -> -18, x=67.5 -> -18, x=-62.7 -> +18,
    #   x=-1.2 -> +18, x=-12.9 -> +18, x=38.8 -> -18, x=73.9 -> -18,
    #   x=-104.0 -> +18, x=-120.7 -> +18
    # Hypothesis (?): sign is +18 when x is negative, -18 when x is positive.
    #   Check: all negatives gave +18, all positives gave -18. Consistent.
    # Sign of zero unknown (?): guess +18.
    out = []
    for x in probe["x"]:
        out.append(18.0 if x <= 0 else -18.0)
    return {"y": out}

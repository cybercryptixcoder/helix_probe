def predict(probe):
    # f(x)=1 for |x|<~1.8, else 0 [E1,E2]
    # E4: at |x|>=1.8 all zero, so upper bound <1.8; E2 shows 1.5->1, 2.0->0
    # So threshold is between 1.5 and 1.8. Guess 1.75. [?]
    out = []
    for x in probe["x"]:
        out.append(1.0 if abs(x) < 1.75 else 0.0)
    return {"y": out}

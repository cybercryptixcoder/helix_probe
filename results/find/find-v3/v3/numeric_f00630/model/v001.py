def predict(probe):
    # Output is one of two constants depending on x [E1]:
    #   x > 0  -> 52.2
    #   x <= 0 -> -14.96
    # Evidence: positive x (88.2,66.0,2.9,72.7,21.3) -> 52.2;
    #           non-positive x (-20.3,-61.7,-24.3,-50.4,-6.0) -> -14.96 [E1]
    # Sign of x is the only distinguishing feature in E1.
    out = []
    for x in probe["x"]:
        out.append(52.2 if x > 0 else -14.96)
    return {"y": out}

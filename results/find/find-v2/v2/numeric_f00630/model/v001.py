def predict(probe):
    # Output is one of two constants: 52.2 or -14.96 [E1]
    # Rule: y = 52.2 when x > 0 (positive), else -14.96 [E1]
    #   x=88.2,66.0,2.9,72.7,21.3 all positive -> 52.2
    #   x=-20.3,-61.7,-24.3,-50.4,-6.0 all negative -> -14.96
    # Sign-based step function; boundary at 0 (untested, assumed) [?]
    out = []
    for x in probe["x"]:
        out.append(52.2 if x > 0 else -14.96)
    return {"y": out}

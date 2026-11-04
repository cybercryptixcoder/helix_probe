def predict(probe):
    # Output is binary: two values, 8.8 and -12.4 (one outlier -11.4) [E1]
    # Sign of x determines output: positive x -> -12.4, negative x -> 8.8 [E1]
    #   x=88.2,66.0,72.7,21.3 (positive) -> -12.4
    #   x=-20.3,-61.7,-24.3,-50.4,-6.0 (negative) -> 8.8
    # x=2.9 (positive) -> -11.4, slight deviation; treat as noise around -12.4 [E1]
    # Model: f(x) = -12.4 if x > 0 else 8.8 (sign function) [?]
    out = []
    for x in probe["x"]:
        out.append(-12.4 if x > 0 else 8.8)
    return {"y": out}

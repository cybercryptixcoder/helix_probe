def predict(probe):
    # Output is +18 or -18 depending on sign of x [E1]
    # Positive x -> -18, negative x -> +18 [E1]
    # (x=2.9 -> -18, x=-6.0 -> +18, x=88.2 -> -18, x=-20.3 -> +18)
    return {"y": [-18.0 if x >= 0 else 18.0 for x in probe["x"]]}

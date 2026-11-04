def predict(probe):
    # For x < -9.375: y ≈ 8 (constant, noisy) [E1, E2, E3, E8]
    # For x >= -9.375: y = 8 - 9.6*x (linear) [E1-E8]
    # E8: -9.4 -> 8.04 (constant), -9.38 -> 98.048 (linear). Boundary in (-9.4, -9.38].
    #   Guess -9.375 (midpoint-ish); both -9.4 and -9.38 fit.
    out = []
    for x in probe["x"]:
        if x < -9.375:
            out.append(8.0)
        else:
            out.append(8.0 - 9.6 * x)
    return {"y": out}

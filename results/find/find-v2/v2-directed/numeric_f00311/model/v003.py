def predict(probe):
    # For x < -9.25: y ≈ 8 (constant, noisy) [E1, E2, E3]
    # For x >= -9.25: y = 8 - 9.6*x (linear) [E1, E2, E3]
    # Boundary: at -9.5 y=7.98 (constant), at -9.25 y=96.8 (linear) [E3]
    #   so transition is between -9.5 and -9.25; guess -9.25 [E3]
    out = []
    for x in probe["x"]:
        if x < -9.25:
            out.append(8.0)
        else:
            out.append(8.0 - 9.6 * x)
    return {"y": out}

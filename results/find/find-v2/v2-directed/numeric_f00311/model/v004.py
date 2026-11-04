def predict(probe):
    # For x < -9.25: y ≈ 8 (constant, noisy) [E1, E2, E3]
    # For x >= -9.25: y = 8 - 9.6*x (linear) [E1, E2, E3, E4]
    # Boundary: at -9.255 y=96.848 (linear), at -9.26 y=96.896 (linear) [E4]
    #   so transition is at or below -9.26; guess -9.25 still fits E4 (all linear)
    # E4 shows all points from -9.3 up are linear, so boundary is <= -9.3
    out = []
    for x in probe["x"]:
        if x < -9.3:
            out.append(8.0)
        else:
            out.append(8.0 - 9.6 * x)
    return {"y": out}

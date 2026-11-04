def predict(probe):
    # For x < -8: y ≈ 8 (constant, noisy) [E1]
    # For x >= -8: y = 8 - 9.6*x (linear) [E1]
    # Boundary between -16 and -8; guessed at -8 [E1]
    out = []
    for x in probe["x"]:
        if x < -8:
            out.append(8.0)
        else:
            out.append(8.0 - 9.6 * x)
    return {"y": out}

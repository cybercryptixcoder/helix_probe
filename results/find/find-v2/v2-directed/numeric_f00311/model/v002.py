def predict(probe):
    # For x < -8: y ≈ 8 (constant, noisy) [E1, E2]
    # For x >= -8: y = 8 - 9.6*x (linear) [E1, E2]
    # Transition is between -9 and -8.75: at -9 y=94.4 (linear), at -8.75 y=92.0 (linear)
    #   and at -9.5 y=8.09 (constant). So boundary is between -9.5 and -9. [E2]
    # Guess boundary at -9: x < -9 -> 8, x >= -9 -> linear. [E2]
    out = []
    for x in probe["x"]:
        if x < -9:
            out.append(8.0)
        else:
            out.append(8.0 - 9.6 * x)
    return {"y": out}

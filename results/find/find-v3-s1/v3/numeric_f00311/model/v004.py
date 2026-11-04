def predict(probe):
    # Rules:
    # For x >= 0: y = 8 - 9.6*x exactly [E2, E4, E3]
    # For -9 <= x < 0: y = 8 - 9.6*x [E4: -0.5->12.8, -5->56; E6: -9->94.4, -8.5->89.6, -5.5->60.8]
    # For x < -9: y ≈ 8 (flat baseline, noisy) [E1, E2, E3, E5, E6: -9.5->8.00, -10->7.96, ...]
    # Boundary between linear and flat on negative side is at x = -9 (E6: -9->94.4 linear, -9.5->8.00 flat)
    out = []
    for x in probe["x"]:
        if x >= -9:
            y = 8 - 9.6 * x
        else:
            y = 8.0
        out.append(round(y, 4))
    return {"y": out}

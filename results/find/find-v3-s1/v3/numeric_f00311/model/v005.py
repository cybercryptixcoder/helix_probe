def predict(probe):
    # For x >= 0: y = 8 - 9.6*x exactly [E2, E4, E3]
    # For -9.4 <= x < 0: y = 8 - 9.6*x exactly [E4, E6, E8: -9.3->97.28 linear]
    # For x < -9.4: y ≈ 8 (flat baseline, noisy) [E1,E2,E3,E5,E6,E7,E8: -9.4->7.90 flat]
    out = []
    for x in probe["x"]:
        if x >= -9.4:
            y = 8 - 9.6 * x
        else:
            y = 8.0
        out.append(round(y, 4))
    return {"y": out}

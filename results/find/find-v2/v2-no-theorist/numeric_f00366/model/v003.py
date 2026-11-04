def predict(probe):
    # Output takes a few discrete values depending on x's sign and magnitude [E1, E2, E3, E4]
    # Positive x: -11.4 for x < 4.2, -12.4 for x >= 4.2 [E2, E4]
    #   E4: 4.1 -> -11.4; 4.2..4.9 -> -12.4
    # Negative x: 9.8 for x > -4.2, 8.8 for x <= -4.2 [E2, E4]
    #   E4: -4.1 -> 9.8; -4.2..-4.9 -> 8.8
    # Threshold is symmetric at |x| = 4.2 (between 4.1 and 4.2) [E4]
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(-11.4 if x < 4.2 else -12.4)
        else:
            out.append(9.8 if -x < 4.2 else 8.8)
    return {"y": out}

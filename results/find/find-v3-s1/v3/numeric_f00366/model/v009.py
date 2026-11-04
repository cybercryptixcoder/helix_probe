import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Beliefs (each line cites evidence):
    # - Output is one of {8.8, 9.8, -11.4, -12.4} for ordinary x [E1,E3,E5,E7,E9,E11,E13,E15].
    # - There is a special point at x = 0.0 returning 1548.92 [E2].
    # - For x < 0: output is 9.8 near zero and 8.8 further out [E4,E6,E8,E12,E14,E16].
    # - For x > 0: output is -11.4 near zero and -12.4 further out [E4,E6,E8,E10,E12,E16].
    # - Negative-side boundary: 9.8 for -4.1 <= x < 0, 8.8 for x < -4.1.
    #   Evidence: -4.1 -> 9.8, -4.101 -> 8.8 [E14,E16]; -4.05 -> 9.8 [E14].
    # - Positive-side boundary: -11.4 for 0 < x <= 4.1, -12.4 for x > 4.1.
    #   Evidence: 4.1 -> -11.4, 4.101 -> -12.4 [E16].
    # - Both boundaries are at |x| = 4.1 (symmetric) [E14,E16].

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue

        if x == 0.0:
            ys.append(1548.92)
            continue

        if x < 0:
            if x >= -4.1:
                ys.append(9.8)
            else:
                ys.append(8.8)
        else:
            if x <= 4.1:
                ys.append(-11.4)
            else:
                ys.append(-12.4)

    return {"y": ys}

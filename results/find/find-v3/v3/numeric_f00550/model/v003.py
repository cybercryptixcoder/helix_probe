def predict(probe):
    # E1,E3: f(x) = -0.0 for |x| >= 1 (ordinary values, including 1.0, -1.0, 1.01, -1.01)
    # E4: nonzero region is exactly the OPEN interval (-1, 1)
    # E2,E4: f(0) = -1.7, f(0.5) = -1.625, f(-0.5) = -3.425
    # E4: values near 0: f(±0.01) ≈ -1.7 (slightly off), f(±0.1) ≈ -1.55/-1.91
    # E4: f(-0.25)=-2.3563, f(0.25)=-1.4562, f(-0.75)=-4.9062, f(0.75)=-2.2062
    # E4: f(±0.9), f(±0.99) are -0.0 -> there is a sub-interval near |x|~0.9 that is zero!
    #   So the nonzero region is NOT all of (-1,1). Looks like |x| < ~0.8 nonzero, else 0.
    #   Check: -0.75 nonzero (-4.9062), -0.9 zero, 0.75 nonzero, 0.9 zero.
    #   Boundary somewhere in (0.75, 0.9). Guess 0.8.
    # Shape: looks like f(x) = -1.7 + something odd-ish. Try f(x) = -1.7 - c*x - d*x^2?
    #   f(0.5)=-1.625 -> -0.5c -0.25d = 0.075
    #   f(-0.5)=-3.425 -> 0.5c -0.25d = -1.725
    #   subtract: -c = 1.8 -> c = -1.8; then -0.25d = 0.075 - 0.9 = -0.825 -> d=3.3
    #   f(x) = -1.7 + 1.8x - 3.3x^2? Check f(0.25): -1.7+0.45-0.20625=-1.45625 ✓ (-1.4562)
    #   Check f(-0.25): -1.7-0.45-0.20625=-2.35625 ✓ (-2.3563)
    #   Check f(0.75): -1.7+1.35-1.85625=-2.20625 ✓ (-2.2062)
    #   Check f(-0.75): -1.7-1.35-1.85625=-4.90625 ✓ (-4.9062)
    #   Check f(0.1): -1.7+0.18-0.033=-1.553 ✓
    #   Check f(-0.1): -1.7-0.18-0.033=-1.913 ✓
    #   Check f(0.01): -1.7+0.018-0.00033=-1.68233 ✓ (-1.6823)
    #   Check f(-0.01): -1.7-0.018-0.00033=-1.71833 ✓ (-1.7183)
    #   Excellent fit! f(x) = -1.7 + 1.8x - 3.3x^2 on |x| < 0.8, else -0.0.
    # ? Boundary in (0.75,0.9); guess 0.8. Need to confirm.
    ys = []
    for x in probe["x"]:
        if x is None:
            ys.append(None)
        elif abs(x) < 0.8:
            ys.append(-1.7 + 1.8 * x - 3.3 * x * x)
        else:
            ys.append(-0.0)
    return {"y": ys}

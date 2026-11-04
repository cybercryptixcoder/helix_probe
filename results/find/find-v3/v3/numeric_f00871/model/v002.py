def predict(probe):
    # f(x) is 0 for most x, but nonzero at some points [E1, E2]
    # Nonzero observed at: x=1.0 -> 2.7, x=-1.0 -> 7.7, x=0.5 -> 3.95,
    #   x=-0.5 -> 6.45, x=0.0 -> 5.2 [E2]
    # Zero at: 10, 100, -10, -100, 50, -50, 3.14159, -2.71828, 127, -127 [E2]
    # Pattern: nonzero only for |x| <= 1 (roughly); value depends on x [E2]
    # Guesses: f(0)=5.2, f(0.5)=3.95, f(-0.5)=6.45, f(1)=2.7, f(-1)=7.7
    # Looks like a linear-ish function on [-1,1]: f(x) ~ 5.2 - 2.5*x ?
    #   f(0.5)=5.2-1.25=3.95 ✓, f(-0.5)=5.2+1.25=6.45 ✓,
    #   f(1)=5.2-2.5=2.7 ✓, f(-1)=5.2+2.5=7.7 ✓
    # So f(x) = 5.2 - 2.5*x for x in [-1,1], else 0. [E2]
    out = []
    for x in probe["x"]:
        if -1.0 <= x <= 1.0:
            out.append(5.2 - 2.5 * x)
        else:
            out.append(0.0)
    return {"y": out}

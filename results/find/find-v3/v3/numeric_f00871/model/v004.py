def predict(probe):
    # f(x) = 5.2 - 2.5*x on [-2.2, 2.1], else 0 [E2, E3, E4]
    # E4: x=2.1 -> -0.05 (linear!), x=2.2 -> 0. So right cutoff is between 2.1 and 2.2.
    # E4: x=-2.1 -> 10.45 (linear!), x=-2.2 -> 0. So left cutoff is between -2.2 and -2.1.
    # E2: x=3.14159 -> 0, x=-2.71828 -> 0 consistent.
    # E3: x=1.2 -> 2.2 consistent.
    # Guess boundaries at 2.15 (right) and -2.15 (left)? Use 2.15 and -2.15.
    out = []
    for x in probe["x"]:
        if -2.15 <= x <= 2.15:
            out.append(5.2 - 2.5 * x)
        else:
            out.append(0.0)
    return {"y": out}

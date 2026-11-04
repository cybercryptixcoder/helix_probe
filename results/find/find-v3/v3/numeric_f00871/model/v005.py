def predict(probe):
    # f(x) = 5.2 - 2.5*x on the linear region, else 0 [E2, E3, E4]
    # E4: x=2.1 -> -0.05 (linear), x=2.2 -> 0. Right cutoff in (2.1, 2.2].
    # E4: x=-2.1 -> 10.45 (linear), x=-2.2 -> 0. Left cutoff in [-2.2, -2.1).
    # E6: x=2.12, 2.14 -> 0; x=-2.12, -2.14 -> 0. So cutoffs are tighter than 2.12.
    #     Combined with E4 (2.1 linear, -2.1 linear), cutoffs lie in (2.1, 2.12] and [-2.12, -2.1).
    # Guess cutoffs at 2.11 and -2.11 (midpoint-ish)? Use 2.11 / -2.11.
    out = []
    for x in probe["x"]:
        if -2.11 <= x <= 2.11:
            out.append(5.2 - 2.5 * x)
        else:
            out.append(0.0)
    return {"y": out}

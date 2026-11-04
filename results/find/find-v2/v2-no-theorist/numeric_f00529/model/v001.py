def predict(probe):
    # Output is ~-6.9 or ~-7.9 depending on x [E1]
    # x=2.9 gives -6.9015, slightly off -6.9 -> suggests a small extra term [E1]
    # Sign pattern: positive x -> -6.9, negative x -> -7.9, except x=2.9 anomaly [E1]
    # Hypothesis: y = -7.4 + 0.5*sign(x) roughly, with a small correction near small |x| [E1]
    # The -6.9015 at x=2.9 hints at a term like -0.0015*|x| or similar small perturbation [E1]
    # ? Boundaries of the sign rule unknown; assume sign(x) with x=0 special
    out = []
    for x in probe.get("x", []):
        if x > 0:
            base = -6.9
        elif x < 0:
            base = -7.9
        else:
            base = -7.4
        # small correction: at x=2.9, -6.9 -> -6.9015, delta -0.0015
        # guess delta = -0.0015 * (x/2.9) for positive small x? uncertain
        # apply a tiny linear correction proportional to x for positives
        if x > 0:
            base = -6.9 - 0.0005 * x
        out.append(base)
    return {"y": out}

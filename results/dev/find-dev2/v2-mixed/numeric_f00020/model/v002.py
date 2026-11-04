def predict(probe):
    # Base level ~81 for ordinary x [E1, E2]
    # Small smooth perturbation around 81 for most x [E2]
    # Sharp rise for x > ~100: 115->84.3, 125->87.9 [E2]
    # Anomaly near x=-5: 81.42 (vs ~80.9 at 0) [E2]
    # Anomaly near x=0: dips to 80.90 [E2]
    # ? The rise for large x looks like a threshold/ramp starting ~105
    # ? The -5 bump is a local feature; unclear shape
    import math
    out = []
    for x in probe["x"]:
        y = 81.0
        # gentle baseline wiggle (small, ~0.01-0.1)
        y += 0.01 * math.sin(x * 0.1)
        # dip near 0
        y -= 0.1 * math.exp(-(x * x) / 50.0)
        # bump near -5
        y += 0.5 * math.exp(-((x + 5) ** 2) / 8.0)
        # ramp for large positive x
        if x > 105:
            y += 0.5 * (x - 105)
        out.append(y)
    return {"y": out}

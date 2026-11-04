def predict(probe):
    # f(x) = 8 - 9.6*x for x >= -9.25 [E2, E3, E4]
    # f(x) ≈ 8 (noisy) for x < -9.25 [E1, E2, E4]
    # Boundary: x=-9.25 gives 96.8 (linear); x=-9.5 gives 7.95 (small) [E4]
    # So switch is in (-9.5, -9.25]; use x < -9.25 -> small, else linear.
    out = []
    for x in probe["x"]:
        if x < -9.25:
            out.append(8.0)
        else:
            out.append(8.0 - 9.6 * x)
    return {"y": out}

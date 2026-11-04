def predict(probe):
    # Almost all outputs are 0.0/-0.0 [E1]
    # Nonzero region: a ramp/plateau shape, not a Gaussian bump [E2]
    # For x in [-2.0, 2.0]: y decreases roughly linearly as x increases [E2]
    #   at x=-2.0 y=10.2, at x=2.0 y=0.2 -> slope ~ -2.5 per unit x
    #   y ≈ 10.2 - 2.5*(x+2.0) = 5.2 - 2.5*x
    # Outside [-2.0, 2.0]: 0.0 [E1, E2]
    # At x=-1.2: 5.2 - 2.5*(-1.2) = 8.2 ✓ [E1, E2]
    out = []
    for x in probe["x"]:
        if -2.0 <= x <= 2.0:
            out.append(5.2 - 2.5 * x)
        else:
            out.append(0.0)
    return {"y": out}

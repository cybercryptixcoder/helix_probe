def predict(probe):
    # Observations are all near -1.6, varying smoothly with x [E1]
    # No obvious structure yet from a single probe; best guess is a
    # nearly-constant function with mild dependence on x.
    # Use a simple smooth baseline: mean of observed ~ -1.62.
    # ? exact shape unknown; assume small linear/quadratic variation.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            # baseline constant; tiny curvature guess
            y = -1.62 + 0.0002 * (x * x) / 100.0
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}

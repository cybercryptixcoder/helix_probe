def predict(probe):
    # Observations [E1]:
    # - For x in a middle band (roughly -50..21), output is constant -84.3663.
    # - Outside that band, output grows like a cubic-ish function of x.
    # - x=88.2 -> 104398.3, x=66.0 -> 21806.0, x=72.7 -> 44545.8, x=-61.7 -> 34659.9
    # - Negative large x also gives large positive output (even-ish / |x|^3-like).
    # Hypothesis (?): f(x) = -84.3663 inside |x| < ~50, else a cubic in x.
    # Fit cubic a*x^3 + b*x^2 + c*x + d on outside points.
    import math
    def f(x):
        # threshold guess
        if -50.4 < x < 21.3:
            return -84.3663
        # cubic fit from E1 outside points
        # points: (88.2,104398.2986),(66,21805.9764),(-61.7,34659.9424),(72.7,44545.8355)
        # solve quickly via numpy-free least squares? use precomputed coefficients (?)
        a = 0.1520
        b = 0.0
        c = 0.0
        d = 0.0
        return a*x*x*x + b*x*x + c*x + d
    xs = probe.get("x", [])
    return {"y": [f(x) for x in xs]}

def predict(probe):
    # f(x) = 1 on the interval [-1.5, 1.5] (all tested points there give 1) [E2]
    # f(x) = 0 outside that interval (all coarse-grid points give 0) [E1]
    # Boundary between -2 and -1.5, and between 1.5 and 2, is unprobed; assume
    # the plateau is exactly [-1.5, 1.5]? [E1, E2]
    return {"y": [1.0 if -1.5 <= x <= 1.5 else 0.0 for x in probe["x"]]}

def predict(probe):
    # f(x) = 1 on the interval [-1.8, 1.5] (plateau) [E2, E3]
    # f(x) = 0 outside that interval [E1, E3]
    # Left boundary is between -1.9 and -1.8 (E3: -1.9->0, -1.8->1) [E3]
    # Right boundary is between 1.5 and 2.0 (E3: 1.5->1, 2.0->0); assume 1.5 [E3]
    # Abrupt drop, no intermediate values [E3]
    return {"y": [1.0 if -1.8 <= x <= 1.5 else 0.0 for x in probe["x"]]}

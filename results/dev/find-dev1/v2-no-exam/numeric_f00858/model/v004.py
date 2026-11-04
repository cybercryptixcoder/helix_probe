def predict(probe):
    # f(x) = 1 on the interval [-1.85, 1.85] (plateau) [E2, E3, E4]
    # f(x) = 0 outside that interval [E1, E3, E4]
    # Left boundary between -1.9 and -1.85 (E4: -1.9->0, -1.85->1) [E4]
    # Right boundary between 1.85 and 1.9 (E4: 1.85->1, 1.9->0) [E4]
    # Abrupt drop, no intermediate values [E3, E4]
    return {"y": [1.0 if -1.85 <= x <= 1.85 else 0.0 for x in probe["x"]]}

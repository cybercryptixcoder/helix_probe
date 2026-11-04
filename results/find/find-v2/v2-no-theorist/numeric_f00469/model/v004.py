def predict(probe):
    # f(x) = 1 for x in [-1.5, 1.5], 0 elsewhere [E2, E3, E4]
    # Left boundary: f(-1.5)=1, f(-2)=0 -> boundary in (-2,-1.5] [E2, E4]
    # Right boundary: f(1.5)=1, f(1.6)=0 -> boundary in [1.5,1.6) [E4]
    # Best guess: closed interval [-1.5, 1.5] [E4]
    return {"y": [1.0 if -1.5 <= x <= 1.5 else 0.0 for x in probe["x"]]}

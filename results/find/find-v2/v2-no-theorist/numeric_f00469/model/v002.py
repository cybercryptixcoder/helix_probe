def predict(probe):
    # f(x) = 1 for x in [-1, 1] (inclusive), 0 elsewhere [E2]
    # Outside that interval f(x) = 0 [E1, E2]
    # Boundaries: f(-1)=1, f(1)=1, f(-2)=0, f(2)=0 [E2]
    return {"y": [1.0 if -1 <= x <= 1 else 0.0 for x in probe["x"]]}

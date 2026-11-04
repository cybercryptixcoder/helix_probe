def predict(probe):
    # f(x) = 1 when |x| is small, else 0 [E2, E3]
    # Nonzero region is symmetric about 0 [E4: -1.6,-1.2,1.2,1.6 -> 1; -2.0,2.0 -> 0]
    # Boundary lies between 1.6 and 2.0 [E4]; E2 shows 1->1, 10->0; E1 shows 2.9->0
    # Pick midpoint ~1.8 as threshold (?)
    def f(x):
        return 1.0 if abs(x) < 1.8 else 0.0
    return {"y": [f(x) for x in probe["x"]]}

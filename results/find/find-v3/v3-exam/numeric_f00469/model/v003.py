def predict(probe):
    # E2: f=1 for x in [-1,2] region, 0 outside (coarse grid)
    # E4: f=1 at -1.5,-1.25,-1.1,-1.0 and 1.5,1.75,1.9; f=0 at 2.0,2.1...
    #     -> left boundary extends below -1 (at least to -1.5); right boundary is between 1.9 and 2.0
    # E1,E3: far values 0
    # Hypothesis: f(x)=1 for -2 <= x < 2 (left edge uncertain, right edge in (1.9,2.0])
    return {"y": [1.0 if -2 <= x < 2 else 0.0 for x in probe["x"]]}

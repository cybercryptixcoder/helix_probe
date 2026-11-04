def predict(probe):
    # f(x) = 2.4*x + 1.8  for x >= 0   [E1: (66,160.2),(88.2,213.48),(72.7,176.28),(21.3,52.92),(2.9,8.76) all exact]
    # f(x) = 2.4*x + 11.7 for x < 0    [E1: (-20.3,-37.02),(-24.3,-46.62),(-50.4,-109.26),(-61.7,-136.38),(-6,-2.7) all exact]
    # Same slope 2.4 both sides; intercept jumps at x=0. Value at exactly 0 unknown; assumed right branch (1.8) [?]
    return {"y": [2.4 * x + (1.8 if x >= 0 else 11.7) for x in probe["x"]]}

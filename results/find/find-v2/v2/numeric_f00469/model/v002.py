def predict(probe):
    # f(x) = 1 for |x| <= 1 (inclusive), else 0 [E2: 0,0.1,-0.1,1,-1,0.5,-0.5 -> 1; 3.7,10,... -> 0]
    # Boundary: |x| <= 1 gives 1; |x| > 1 gives 0 [E2]
    # E1 all |x|>1 -> 0, consistent [E1]
    return {"y": [1.0 if abs(x) <= 1.0 else 0.0 for x in probe["x"]]}

def predict(probe):
    # f(x) = 1 for |x| <= 1 (inclusive), else 0 [E2: 0,0.1,-0.1,1,-1,0.5,-0.5 -> 1; 3.7,10,... -> 0]
    # Boundary: |x| <= 1 gives 1; |x| > 1 gives 0 [E2]
    # E1 all |x|>1 -> 0, consistent [E1]
    # E3: x=1.2 -> 1, so boundary is wider than 1; |x|<=1.2 gives 1? [E3]
    # E2 had 1.0->1 and 3.7->0; E3 has 1.2->1. So threshold is between 1.2 and 3.7.
    # Best guess: |x| <= 1.5 (?) [E2,E3]
    return {"y": [1.0 if abs(x) <= 1.5 else 0.0 for x in probe["x"]]}

def predict(probe):
    # All observed outputs are 0.0 or -0.0 across a wide range of x [E1]
    # No evidence of any nonzero output yet; simplest hypothesis is f(x)=0
    return {"y": [0.0 for _ in probe["x"]]}

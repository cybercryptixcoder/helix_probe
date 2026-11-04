def predict(probe):
    # f(x) is nearly constant ~81 across the whole domain [-128,128] [E1]
    # Small deviations (~0.08 max) look like noise/MLP wiggle, not structure [E1]
    # Best guess: constant 81.0 [E1]
    xs = probe.get("x", [])
    return {"y": [81.0 for _ in xs]}

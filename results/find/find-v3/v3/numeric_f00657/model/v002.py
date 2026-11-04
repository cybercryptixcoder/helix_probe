def predict(probe):
    # Output is +18 for x < 0, -18 for x > 0 [E1, E2]
    # x = 0 gives +18 (so the rule is: -18 if x > 0 else +18) [E2]
    return {"y": [-18.0 if x > 0 else 18.0 for x in probe["x"]]}

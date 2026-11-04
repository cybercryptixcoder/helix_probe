def predict(probe):
    # Output takes one of two values: -14.96 or 52.2 [E1]
    # Positive x -> 52.2; negative x -> -14.96 [E1]
    # (sign-based step function)
    return {"y": [52.2 if x > 0 else -14.96 for x in probe["x"]]}

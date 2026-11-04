def predict(probe):
    # Constant function: f(x) = 53 for all tested x [E1]
    # ? Only one experiment so far; assume constant everywhere.
    xs = probe.get("x", [])
    return {"y": [53.0 for _ in xs]}

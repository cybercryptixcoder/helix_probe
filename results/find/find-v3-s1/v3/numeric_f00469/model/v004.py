def predict(probe):
    # f(x) = 1 exactly when |x| <= 1.5, else 0 [E2, E5, E6, E7, E8]
    # Boundary: 1.5 -> 1, 1.52 -> 0; -1.5 -> 1, -1.52 -> 0 [E8]
    # So threshold is 1.5 inclusive.
    out = []
    for x in probe["x"]:
        out.append(1.0 if abs(x) <= 1.5 else 0.0)
    return {"y": out}

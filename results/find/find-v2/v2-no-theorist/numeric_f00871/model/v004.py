def predict(probe):
    # f(x) = 5.2 - 2.5*x for |x| <= 2.1, else 0 [E2, E4, E6]
    # Boundary inclusive: x=2.1 -> -0.05, x=-2.1 -> 10.45 [E6]
    # Outside |x|>2.1: exactly 0 [E1, E2, E3, E5, E6]
    out = []
    for x in probe["x"]:
        out.append(5.2 - 2.5 * x if abs(x) <= 2.1 else 0.0)
    return {"y": out}

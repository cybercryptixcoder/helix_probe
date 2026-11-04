def predict(probe):
    # f(x) = 5.2 - 2.5*x for |x| <= 2.1, else 0 [E2, E4, E6, E8]
    # Boundary inclusive: x=2.1 -> -0.05, x=-2.1 -> 10.45 [E6]
    # Outside |x|>2.1: 0, EXCEPT a noisy band near x in [-80,-78] [E9, E10]
    # In that band values are ~0.1-0.4, noisy, no clear structure -> model as
    #   a noisy region: return a fixed mid value (noise can't be predicted) [E10]
    out = []
    for x in probe["x"]:
        if abs(x) <= 2.1:
            out.append(5.2 - 2.5 * x)
        elif -80.0 <= x <= -78.0:
            # noisy band: observed values range ~[-0.13, 0.39], mean ~0.12 [E10]
            out.append(0.12)
        else:
            out.append(0.0)
    return {"y": out}

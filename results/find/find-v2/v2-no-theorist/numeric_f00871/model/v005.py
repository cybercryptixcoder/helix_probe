def predict(probe):
    # f(x) = 5.2 - 2.5*x for |x| <= 2.1, else 0 [E2, E4, E6, E8]
    # Boundary inclusive: x=2.1 -> -0.05, x=-2.1 -> 10.45 [E6]
    # Outside |x|>2.1: mostly 0, but there is a narrow nonzero spike near x=-79.1 [E9]
    # Spike at x=-79.1 gives 0.1388; unknown width/shape, model as narrow window [E9]
    out = []
    for x in probe["x"]:
        if abs(x) <= 2.1:
            out.append(5.2 - 2.5 * x)
        elif -79.2 <= x <= -79.0:
            # narrow spike observed at -79.1 -> 0.1388; width/shape unknown (?)
            out.append(0.1388)
        else:
            out.append(0.0)
    return {"y": out}

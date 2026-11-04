def predict(probe):
    # f(x) = 5.2 - 2.5*x for |x| <= 2.1, else 0 [E2, E4, E6, E8]
    # Boundary inclusive: x=2.1 -> -0.05, x=-2.1 -> 10.45 [E6]
    # Outside |x|>2.1: 0, EXCEPT a noisy band over roughly x in [-84,-77] [E9,E10,E12,E14]
    # Band values are noisy ~0.0-0.4, no clear structure -> return a fixed mid value [E10,E12,E14]
    # Edges: nonzero at -84..-78.1, zero at -77.2 and below; left edge uncertain (>= -84) [?]
    out = []
    for x in probe["x"]:
        if abs(x) <= 2.1:
            out.append(5.2 - 2.5 * x)
        elif -84.0 <= x <= -78.0:
            out.append(0.12)
        else:
            out.append(0.0)
    return {"y": out}

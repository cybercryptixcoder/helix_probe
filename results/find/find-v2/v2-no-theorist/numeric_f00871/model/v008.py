def predict(probe):
    # f(x) = 5.2 - 2.5*x for |x| <= 2.1, else 0 [E2, E4, E6, E8]
    # Boundary inclusive: x=2.1 -> -0.05, x=-2.1 -> 10.45 [E6]
    # Outside |x|>2.1: 0, EXCEPT a noisy band over x in [-88.25, -77.9] [E20,E22,E24]
    # Band values are noisy ~0.0-0.35, no clear structure -> return a fixed mid value [E10,E12,E14,E16,E18,E20,E22,E24]
    # Left edge: nonzero at -88.25, zero at -88.5 [E24]; right edge: nonzero at -77.9, zero at -77.55 [E24]
    out = []
    for x in probe["x"]:
        if abs(x) <= 2.1:
            out.append(5.2 - 2.5 * x)
        elif -88.25 <= x <= -77.9:
            out.append(0.12)
        else:
            out.append(0.0)
    return {"y": out}

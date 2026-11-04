def predict(probe):
    # f(x) = 5.2 - 2.5*x for |x| < 2.1, else 0 [E2, E3, E4]
    # Linear slope -2.5 confirmed across [0,2.05] and [-2.05,0] [E2, E4]
    # Nonzero region: |x| < 2.1 (x=2.1 -> -0.05 nonzero, x=2.2 -> 0) [E4]
    # For x<0 boundary: x=-2.1 -> 10.45 nonzero, x=-2.2 -> 0 [E4]
    # So threshold T = 2.1 (open interval |x| < 2.1) [E4]
    # Outside: exactly 0 [E1, E2, E3]
    T = 2.1
    out = []
    for x in probe["x"]:
        if abs(x) < T:
            out.append(5.2 - 2.5 * x)
        else:
            out.append(0.0)
    return {"y": out}

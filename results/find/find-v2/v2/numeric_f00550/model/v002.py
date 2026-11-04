def predict(probe):
    # f(x) = 0 for all x except near 0 [E1, E2]
    # Nonzero values only observed for |x| < 1: f(-0.5)=-3.425, f(0.5)=-1.625, f(0)=-1.7 [E2]
    # Looks like a narrow spike/dip around x=0; magnitude decreases with |x| [E2]
    # Model: a triangular/parabolic dip centered at 0 with half-width 1, zero outside [E2, ?]
    # Peak depth ~ -3.425 at x=-0.5, -1.7 at 0, -1.625 at 0.5 — asymmetric, unclear [E2, ?]
    # Best guess: linear-ish dip, f(x) = -1.7 - 3.45*|x| for |x|<1, else 0 [E2, ?]
    out = []
    for x in probe["x"]:
        if abs(x) < 1.0:
            out.append(-1.7 - 3.45 * abs(x))
        else:
            out.append(0.0)
    return {"y": out}

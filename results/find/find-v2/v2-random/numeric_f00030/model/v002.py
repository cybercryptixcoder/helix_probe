def predict(probe):
    # Observations cluster near -1.6 with smooth variation [E1, E2]
    # y decreases as |x| grows toward mid-range, rises again at large |x| [E1, E2]
    # At x near 0, y is most negative (~-1.75 at x=1.2) [E2]
    # At large |x| (~100+), y rises toward ~-1.52 [E2]
    # Looks like a smooth even-ish function: minimum near x=0, rising with |x|
    # ? model as quadratic in x with negative curvature near 0 flipping at large |x|
    # ? simplest: y = a + b*cos-like; try y = c0 + c1*x^2 - c2*x^4 shape
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            # Fit: at x=0 ~ -1.76, at |x|=100 ~ -1.53, at |x|=50 ~ -1.59
            # quadratic in x^2: y = A + B*u + C*u^2, u = (x/100)^2
            u = (x / 100.0) ** 2
            y = -1.76 + 0.55 * u - 0.30 * u * u
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}

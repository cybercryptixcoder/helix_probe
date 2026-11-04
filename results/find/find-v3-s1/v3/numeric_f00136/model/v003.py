import math

def predict(probe):
    # f(x) is smooth in x alone [E2].
    # For x <= -20: y decreases with slope ~0.00029 per unit [E2].
    # For x >= -20: y rises with slope ~0.00029 per unit [E2].
    # V-shape with minimum near x=-20 [E2].
    # E1/E3 show large residuals around x in [-15,10]: there is a dip/bump
    #   near x=0 (E2: y=-0.0008 at 0, -0.0405 at 5, -0.0249 at 10, 0.055 at -5)
    #   suggesting a localized negative dip centered near x~5 [E2].
    # ? Model: base V-shape plus a Gaussian dip centered at x=5, width ~8,
    #   amplitude ~-0.05, to capture the special interval near 0 [E2].
    xs = probe.get("x", [])
    out = []
    for x in xs:
        base = 0.0162 + 0.00029 * abs(x + 20)
        dip = -0.055 * math.exp(-((x - 5.0) ** 2) / (2 * 8.0 ** 2))
        out.append(base + dip)
    return {"y": out}

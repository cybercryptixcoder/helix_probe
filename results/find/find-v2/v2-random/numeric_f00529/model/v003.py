import math

def predict(probe):
    # The box computes: y = -7.9 + 1/(1 + exp(-4.65*(x - 1.5)))
    # For x well below 1.5, sigmoid≈0 so y≈-7.9 [E1-E6 all negatives]
    # For x well above 1.5, sigmoid≈1 so y≈-6.9 [E1-E6 all positives]
    # Smooth transition centered at x=1.5 with slope 4.65:
    #   x=1.2 -> -7.7016, x=2.0 -> -6.9889, x=2.9 -> -6.9015 [E2, E6, E1]
    #   (logit fit gives k≈4.65, x0≈1.5 consistently across all three)
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            xf = float(x)
            s = 1.0 / (1.0 + math.exp(-4.65 * (xf - 1.5)))
            ys.append(-7.9 + s)
        except Exception:
            ys.append(None)
    return {"y": ys}

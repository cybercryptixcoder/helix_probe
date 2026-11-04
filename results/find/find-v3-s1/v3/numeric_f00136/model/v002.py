import math

def predict(probe):
    # f(x) is a smooth function of x alone [E2]: dense grid shows a clear trend.
    # For x <= -20: y decreases roughly linearly with slope ~0.00029 per unit
    #   (0.0455 at -120 down to 0.0162 at -20) [E2].
    # For x >= -20: y rises roughly linearly with slope ~0.00029 per unit
    #   (0.0162 at -20 up to 0.0565 at 128) [E2].
    # So f(x) = a + b*|x - (-20)|, a V-shape with minimum near x=-20 [E2].
    # Fit: a ~ 0.0162 at x=-20; b ~ 0.00029.
    # E1 values are noisy but roughly consistent with this V-shape [E1, E2].
    # ? The V-shape is a guess; the minimum location and slopes are approximate.
    xs = probe.get("x", [])
    out = []
    for x in xs:
        out.append(0.0162 + 0.00029 * abs(x + 20))
    return {"y": out}

import math

def predict(probe):
    # Beliefs (from the evidence):
    # - For x >= ~20, f is essentially linear with slope ~0.00055 and intercept ~ -0.0153 [E2, E6]
    # - For x <= ~-20, f is also linear but with slope ~ -0.00029 and intercept ~0.0105 [E2, E6]
    # - There is a central "bump" region roughly -20 < x < 20 where f deviates strongly:
    #   a sharp positive spike near x=-2..-4 and a sharp negative dip near x=2..4 [E4]
    # - At x=0, f ~ -0.0008 (near zero, not on either outer line) [E2, E4]
    # - The central region is smooth-ish but asymmetric; we approximate with a
    #   piecewise model: outer linear tails + a localized odd-ish bump.
    # - Noise is small; outputs are smooth in x. [all E]
    x = probe["x"]
    ys = []
    for v in x:
        ys.append(_f(v))
    return {"y": ys}

def _f(x):
    # Outer left tail: x <= -20
    # Fit from E2/E6: at x=-20 y=0.0162, x=-30 y=0.0191, x=-120 y=0.0455
    # slope ~ (0.0455-0.0162)/(-120+20)= -0.000293, intercept ~0.01034
    # Right tail: x >= 20
    # x=20 y=-0.0043, x=120 y=0.0522 => slope ~0.000565, intercept ~ -0.0156
    # Central: use interpolation through observed shape.
    if x <= -20:
        return 0.01034 - 0.000293 * x
    if x >= 20:
        return -0.0156 + 0.000565 * x

    # Central region (-20, 20): build a smooth curve matching E4/E6/E2 points.
    # Key anchor points (x, y):
    # -20: 0.0162, -19: 0.0159, -17: 0.0152, -15: 0.0146, -12: 0.0187,
    # -10: 0.0249, -8: 0.031, -6: 0.0471, -4: 0.0628, -2: 0.0784,
    # 0: -0.0008, 2: -0.0595, 4: -0.0438, 5: -0.0405, 6: -0.0371,
    # 8: -0.03, 10: -0.0249, 12: -0.0208, 15: -0.0146, 18: -0.0084,
    # 20: -0.0043
    # Use piecewise linear interpolation on these anchors for simplicity.
    anchors = [
        (-20, 0.0162), (-19, 0.0159), (-17, 0.0152), (-15, 0.0146),
        (-12, 0.0187), (-10, 0.0249), (-8, 0.031), (-6, 0.0471),
        (-4, 0.0628), (-2, 0.0784), (0, -0.0008), (2, -0.0595),
        (4, -0.0438), (5, -0.0405), (6, -0.0371), (8, -0.03),
        (10, -0.0249), (12, -0.0208), (15, -0.0146), (18, -0.0084),
        (20, -0.0043)
    ]
    # find bracketing anchors
    for i in range(len(anchors) - 1):
        x0, y0 = anchors[i]
        x1, y1 = anchors[i + 1]
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    # fallback (shouldn't happen)
    return 0.0

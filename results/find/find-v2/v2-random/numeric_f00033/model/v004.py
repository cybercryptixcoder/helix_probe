import math

def predict(probe):
    # Beliefs (revised):
    # - f(x) is ~0 (|y|<1e-3) for x > ~5, decaying to ~-1e-4 far positive [E1-E7]
    # - There is a positive bump near x≈0: f(1.2)=0.228, f(2.0)=0.12, f(2.9)=0.036,
    #   f(-1.6)=0.092, f(-5.9)=0.0003 [E1,E2,E4,E5,E6]
    # - The bump is asymmetric: peak ~0.23 near x≈1.2, wider/taller on the
    #   negative side (f(-1.6)=0.092 vs f(2.9)=0.036) [E1,E5,E6]
    # - For x < ~-10 there is a shallow negative baseline ~-0.003 to -0.0045,
    #   roughly flat, slightly deeper near x≈-50 to -125 [E1,E3,E4,E5,E6,E7]
    # - For x in ~[-10, 5] the function is dominated by the bump (positive)
    # - For x > ~5 the value is ~0 to -1e-4 (near zero, slightly negative) [E1-E7]
    # - Output is smooth (MLP); use smooth basis functions

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue

        # Positive central bump, asymmetric Gaussian.
        # Peak ~0.23 at x0≈1.1; sigma_left ~2.2, sigma_right ~1.4
        x0 = 1.1
        if x < x0:
            sigma = 2.2
        else:
            sigma = 1.4
        bump = 0.23 * math.exp(-((x - x0) ** 2) / (2 * sigma ** 2))

        # Negative baseline on the left (x < ~-8), roughly flat ~-0.0035,
        # slightly deeper toward very negative x.
        # Use a smooth step (sigmoid) to turn it on for x < -8.
        left_gate = 1.0 / (1.0 + math.exp((x + 8.0) / 1.5))
        base_left = -0.0033 * left_gate
        # Slight extra depth near x≈-60 to -125
        base_left += -0.0008 * math.exp(-((x + 90.0) ** 2) / (2 * 40.0 ** 2)) * left_gate

        # Near-zero slightly negative floor for x > ~5
        right_gate = 1.0 / (1.0 + math.exp(-(x - 5.0) / 1.5))
        base_right = -0.0002 * right_gate

        y = bump + base_left + base_right
        ys.append(y)

    return {"y": ys}

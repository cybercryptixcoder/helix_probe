import math

def predict(probe):
    # Beliefs:
    # - Central positive bump near x≈0..2, peak ~0.23 at x≈1.2 [E1,E2,E5,E6]
    # - Bump asymmetric: wider on negative side (f(-1.6)=0.092) than positive (f(2.9)=0.036) [E1,E5,E6]
    # - For x>~5: ~0, tiny negative (-1e-4..-3e-4) [E1-E8]
    # - For x<-~10: shallow negative baseline ~-0.003 to -0.0045 [E1-E8]
    # - Near x≈-6 to -7: value ~0 (bump tail cancels baseline) [E1,E3,E8]
    # - Some noise in the -0.001..-0.006 band for mid-negative x [E6,E7]

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue

        # Asymmetric Gaussian bump, peak ~0.23 at x0≈1.1
        x0 = 1.1
        sigma = 2.2 if x < x0 else 1.4
        bump = 0.23 * math.exp(-((x - x0) ** 2) / (2 * sigma ** 2))

        # Left negative baseline, turns on for x < ~-8
        left_gate = 1.0 / (1.0 + math.exp((x + 8.0) / 1.5))
        base_left = -0.0033 * left_gate
        base_left += -0.0008 * math.exp(-((x + 90.0) ** 2) / (2 * 40.0 ** 2)) * left_gate

        # Right near-zero slightly negative floor for x > ~5
        right_gate = 1.0 / (1.0 + math.exp(-(x - 5.0) / 1.5))
        base_right = -0.0002 * right_gate

        y = bump + base_left + base_right
        ys.append(y)

    return {"y": ys}

import math

def predict(probe):
    # Beliefs:
    # - f(x) is near zero (about -1e-4 to -4e-3) for most |x| > ~5 [E1-E5]
    # - There is a narrow positive "bump" around x ≈ 0: f(1.2)=0.228, f(2.9)=0.0362,
    #   f(-1.6)=0.0919, f(-5.9)=0.0003 [E1,E2,E4,E5]
    # - The bump is roughly Gaussian/even-ish, peaked near x≈1, decaying fast
    #   by |x|≈5-6 [E1,E2,E5]
    # - Outside the bump, the small negative baseline varies slowly with x
    #   (roughly -0.003 to -0.004), likely a broad shallow negative lobe
    #   centered somewhere negative-ish [E1-E5]
    # - No sign of a sharp interval boundary other than the bump region [E1-E5]
    # - Output is smooth; MLP approximation => use smooth basis functions

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue

        # Positive central bump: Gaussian centered near x0, width sigma
        # Peak ~0.23 at x≈1.2; f(2.9)=0.036 => sigma ≈ 1.3-1.5
        # f(-1.6)=0.092 consistent with center ~1.0, sigma ~1.6
        x0 = 1.0
        sigma = 1.6
        bump = 0.23 * math.exp(-((x - x0) ** 2) / (2 * sigma ** 2))

        # Broad shallow negative baseline, slowly varying.
        # Values ~ -0.0032 at |x|~50-65, ~ -0.0002 at |x|~90-120,
        # ~ -0.004 at x≈-48, -102, -124; ~ -0.001 at x≈-17.
        # Model as a wide negative Gaussian centered near x≈-60 with
        # amplitude ~ -0.0035 and sigma ~ 45, plus slight offset.
        base = -0.0035 * math.exp(-((x + 60.0) ** 2) / (2 * 45.0 ** 2))
        # Slight additional negative near large negative x
        base += -0.0010 * math.exp(-((x + 110.0) ** 2) / (2 * 25.0 ** 2))
        # Very small positive/zero floor far away
        # (keeps values near -1e-4 at large positive x)
        base += -0.0001

        y = bump + base
        ys.append(y)

    return {"y": ys}

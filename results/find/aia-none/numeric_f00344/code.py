
def f(x):
    if x == 0:
        return 472.73

    # Baseline quartic polynomial that holds away from the origin
    base = -1.2*x**4 - 3*x**3 + 0.9*x**2 - 4*x - 24.25

    # Localized disruption in the interval roughly (-4, 4)
    if 0 < x < 3.5:
        # Right side: smoothly lowered, blending back by ~3.5
        t = x / 3.5                       # 0..1
        # near x->0+ value is ~ -36.8; blends into base by t->1
        lowered = (1 - t) * (-36.8) + t * base
        return lowered
    if -4.0 < x < 0:
        # Left side: raised hump peaking near x = -2.12 (value ~0.074)
        # Use base, shifted up by a bell-shaped bump around x = -2.12
        bump = 0.074 * (1 - ((x + 2.12) / 2.0)**2)
        if bump < 0:
            bump = 0.0
        return base + bump
    return base

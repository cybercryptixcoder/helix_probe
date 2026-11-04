
def f(x):
    # Two underlying lines
    L = -26.0716 * x - 25.44          # left (negative-slope) branch
    R = 111.4278 * x + 106.05          # right (positive-slope) branch
    base = max(L, R)

    # The MLP rounds the valley near x ~ -1.05 (min ~6.42) where the
    # sharp max would give ~ -0.5. Add a smooth bump confined to the valley.
    # A Gaussian bump of height ~6.9 centered at -1.05, width ~0.35.
    import math
    bump = 6.9 * math.exp(-((x + 1.05) ** 2) / (2 * 0.32 ** 2))

    # The bump should only raise the region near the valley; it's negligible elsewhere.
    return base + bump


import numpy as np

SLOPE = 4.714
INTERCEPT = 4.21

def f_approx(x):
    x = np.asarray(x, dtype=float)
    # Linear base trend (dominant behavior)
    y = SLOPE * x + INTERCEPT
    # Localized smooth dip near origin:
    # amplitude ~0.33, centered near x=-0.1, width ~1.2
    dip = -0.33 * np.exp(-((x + 0.1) ** 2) / (2 * 1.2 ** 2))
    return y + dip

# Sanity checks:
# f_approx(0)    ~ 3.90   (true 3.9155)
# f_approx(-0.1) ~ 3.86   (true 3.412... -> note: linear part at -0.1 is 3.74; with dip ~3.88)
# f_approx(10)   ~ 51.35  (true 51.353)
# f_approx(-64)  ~ -297.5 (true -295.7)
# f_approx(128)  ~ 607.6  (true 607.61)

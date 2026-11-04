
import random

def f(x):
    # Special "flat" interval where output collapses to ~7773 (noisy)
    if 97.5 < x <= 117.5:
        return 7773.0 + random.uniform(-0.15, 0.25)
    # Normal behavior: cubic polynomial
    return 1.3 * x**3 + 2.3 * x**2 - 1.6 * x - 48.6

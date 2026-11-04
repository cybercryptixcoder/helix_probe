
import math, random

def f(x):
    # deterministic sigmoid ramp: low 0.3 -> high 12.5, midpoint ~ x0=-5
    low, high = 0.3, 12.5
    x0, k = -5.0, 0.6
    base = low + (high - low) / (1.0 + math.exp(-k * (x - x0)))
    # heavy additive noise (occasionally several units, sometimes negative on low side)
    noise = random.gauss(0, 1.8) + random.gauss(0, 0.8)
    return base + noise

# Approximate deterministic part only (ignoring noise):
def f_mean(x):
    return 0.3 + 12.2 / (1.0 + math.exp(-0.6 * (x + 5.0)))

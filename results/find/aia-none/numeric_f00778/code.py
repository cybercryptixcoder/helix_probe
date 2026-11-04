
import random

def f(x):
    # Clean underlying cubic approximation
    poly = -3.9 * x**3 - 0.2 * x**2 + 1.7 * x + 3.2
    # Additive noise, roughly constant magnitude (~std 0.8).
    # Near x=0 this dominates since poly ~ small there.
    noise = random.gauss(0, 0.8)
    return poly + noise

# Examples (clean values, noise excluded):
# f(10)  ≈ -3897.7   (model -3899.8)
# f(50)  ≈ -487897   (model -487893)
# f(-30) ≈ +105062   (model +105071)
# f(0)   ≈ 3.2 ± ~1  (noisy)

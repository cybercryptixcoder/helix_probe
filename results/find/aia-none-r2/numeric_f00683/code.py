
import random

def f(x):
    noise = random.uniform(-1.5, 1.5)  # output is a bit noisy
    if x == 0:
        # isolated spike at exactly x = 0
        return -384.12 + random.uniform(-1, 1)
    elif x > 0:
        return 13.1 * x - 5.5 + noise
    else:  # x < 0
        return 1.32 * x - 10.0 + noise

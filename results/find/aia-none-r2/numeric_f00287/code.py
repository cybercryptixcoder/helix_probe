
import random

def f(x):
    if x <= -5.1:
        return -0.7 * x
    elif x >= 18.515:
        return -16.8 * x
    else:
        # flat noisy plateau
        return -402.3 + random.uniform(-0.15, 0.15)

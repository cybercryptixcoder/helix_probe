
import random

def f(x):
    # small measurement noise
    noise = random.uniform(-1.5, 1.5)
    if x == 0:
        # special anomalous value near x = 0
        return -384.0 + noise
    elif x > 0:
        # steep positive branch, slope ~13
        return 13.0 * x - 5.0 + noise
    else:
        # shallow negative branch, slope ~1.3
        return 1.3 * x - 13.0 + noise

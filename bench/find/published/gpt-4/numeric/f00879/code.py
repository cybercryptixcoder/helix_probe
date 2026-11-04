
import random

def approximate_function(x):
    noise = random.uniform(-0.5, 0.5)
    if x < 0:
        return -1 + noise
    else:
        return 1 + noise


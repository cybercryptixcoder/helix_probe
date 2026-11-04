
import random

def f(x):
    if x < 103:
        return x
    else:
        return random.random()  # random value in [0, 1)

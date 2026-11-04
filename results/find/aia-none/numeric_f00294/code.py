
import math

def f(x):
    if x == 0:
        return 2058.0
    elif x > 0:
        return math.ceil(x) + 16.8
    else:  # x < 0
        return math.ceil(x) - 8.4

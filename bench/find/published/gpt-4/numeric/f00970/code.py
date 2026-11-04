
import math

def approximate_function(x):
    if x == 0:
        return 10
    return -math.exp(math.log(abs(x)) - 1) + 10

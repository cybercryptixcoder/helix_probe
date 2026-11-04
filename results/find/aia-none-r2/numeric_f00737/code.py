
import math

def f(x):
    # Matches observed behavior: natural log, scaled + shifted.
    # x < 0 -> nan ; x == 0 -> -inf ; x > 0 -> a*ln(x) + b
    a = 9.1023649454
    b = -7.8
    if x < 0:
        return float('nan')
    if x == 0:
        return float('-inf')
    return a * math.log(x) + b


import math

def f(x):
    if -4.35 <= x <= 4.35:
        if x > 0:
            return float(math.ceil(x))
        elif x < 0:
            return float(math.trunc(x))   # truncates toward zero
        else:
            return 0.0
    else:
        # outside [-4.35, 4.35]: return signed zero
        return math.copysign(0.0, x)

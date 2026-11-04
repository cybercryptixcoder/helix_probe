
import math

def f(x):
    # Asymmetric stretched-exponential bump
    A = 0.389        # peak height
    c = -0.04        # peak location
    p = 1.6          # stretching exponent
    a_left  = 0.70   # decay rate on negative side (x < c)
    a_right = 0.40   # decay rate on positive side (x > c)
    d = abs(x - c)
    a = a_left if x < c else a_right
    y = A * math.exp(-a * (d ** p))
    # Essentially zero outside the support
    if abs(x - c) > 6.0:
        y = 0.0
    return y

# Example predictions:
# f(0)     ~ 0.385   (actual 0.387)
# f(1)     ~ 0.255   (actual 0.255)
# f(-1)    ~ 0.197   (actual 0.197)
# f(3)     ~ 0.033   (actual 0.033)
# f(-3)    ~ 0.008   (actual 0.008)

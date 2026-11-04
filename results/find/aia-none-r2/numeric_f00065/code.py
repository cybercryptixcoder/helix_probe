
import math

def f_approx(x):
    # Two underlying lines, both passing near (0, -8.59)
    L_A = -8.59 - 2.499 * x   # steep line, dominates for x > 0
    L_B = -8.59 - 1.752 * x   # shallow line, dominates for x < 0

    # Smooth minimum (softmin) of the two lines.
    # p controls sharpness of the rounded corner near x = 0.
    p = 8.45
    # softmin(a,b) = -log(exp(-p*a) + exp(-p*b)) / p  (numerically stable)
    m = min(L_A, L_B)
    sm = m - math.log(math.exp(-p * (L_A - m)) + math.exp(-p * (L_B - m))) / p
    return sm

# Equivalent pointwise result:
#  x -> -2.499*x - 8.59  for large positive x
#  x -> -1.752*x - 8.59  for large negative x
#  smooth rounded corner in ~[-2, 2], sagging to ~ -8.67 at x = 0

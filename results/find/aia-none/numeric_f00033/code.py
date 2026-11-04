
import math

def f(x):
    A = 0.3867882830559317      # peak value at x = 0
    sigma_right = 1.31          # positive side width
    sigma_left  = 1.02          # negative side width
    sigma = sigma_right if x >= 0 else sigma_left
    # asymmetric Gaussian bump centered at 0
    return A * math.exp(-x * x / (2.0 * sigma * sigma))

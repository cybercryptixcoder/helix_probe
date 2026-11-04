
import math

def f(x):
    if x < 0:
        return float('nan')
    if x == 0:
        return float('-inf')
    a = 9.1026   # ≈ 9.1026 (precise value ~9.1026)
    b = -7.8     # exact (f(1) = -7.8)
    return a * math.log(x) + b

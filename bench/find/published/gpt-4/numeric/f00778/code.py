
def approx_f(x):
    if x > 0:
        return -x**3 - (0.1 * x**2) + 0.5
    else:
        return x**3 + (0.1 * x**2) - 0.5
